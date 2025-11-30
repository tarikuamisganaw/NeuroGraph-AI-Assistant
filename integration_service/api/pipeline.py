"""Pipeline API endpoints."""  
import os  
import tempfile  
from typing import List  
from fastapi import APIRouter, UploadFile, File, Form, HTTPException  
from ..services.orchestration_service import OrchestrationService  
from ..config.settings import settings  
  
router = APIRouter()  
orchestration_service = OrchestrationService()  
  
@router.post("/execute")  
@router.post("/execute")  
async def execute_pipeline(  
    files: List[UploadFile] = File(...),  
    config: str = Form(...),  
    schema_json: str = Form(...),  
    writer_type: str = Form("networkx")  # Add this parameter  
):  
    """Execute complete pipeline: CSV → NetworkX → Miner."""  
      
    # Save uploaded files to temporary directory  
    with tempfile.TemporaryDirectory() as temp_dir:  
        csv_files = []  
        for file in files:  
            file_path = os.path.join(temp_dir, file.filename)  
            with open(file_path, "wb") as f:  
                content = await file.read()  
                f.write(content)  
            csv_files.append(file_path)  
          
        # Use first CSV file for processing  
        csv_file_path = csv_files[0]  
          
        # Generate NetworkX graph  
        networkx_result = await orchestration_service._generate_networkx(  
            csv_file_path=csv_file_path,  
            config=config,  
            schema_json=schema_json,  
            writer_type=writer_type  # Pass the writer_type  
        )  
          
        # Mine motifs  
        motifs = await orchestration_service._mine_motifs(  
            networkx_result["networkx_file"]  
        )  
          
        return {  
            "job_id": networkx_result["job_id"],  
            "motifs": motifs,  
            "status": "success"  
        }
  
@router.post("/select-motif")  
async def select_motif(  
    job_id: str = Form(...),  
    motif_index: int = Form(...),  
    tenant_id: str = Form("default")  
):  
    """User selects a motif for processing."""  
    try:  
        result = await orchestration_service.process_selected_motif(  
            job_id=job_id,  
            motif_index=motif_index,  
            tenant_id=tenant_id  
        )  
        return result  
    except Exception as e:  
        raise HTTPException(status_code=500, detail=str(e))