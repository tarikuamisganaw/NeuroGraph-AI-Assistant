"""Main orchestration service for pipeline coordination."""  
import os  
import uuid  
import httpx  
import tempfile  
import json  
from typing import Dict, Any, List  
from .miner_service import MinerService  
from ..config.settings import settings  
  
class OrchestrationService:  
    """Main pipeline orchestrator."""  
        self,  
        job_id: str,  
        motif_index: int,  
        tenant_id: str = "default"  
    ) -> Dict[str, Any]:  
        """Process user-selected motif."""  
        try:  
            return {  
                "job_id": job_id,  
                "status": "motif_selected",  
                "motif_index": motif_index,  
                "message": "Motif selection received. Ready for Phase 2 processing."  
            }  
        except Exception as e:  
            return {"job_id": job_id, "status": "error", "error": str(e)}  
          
    async def _generate_networkx(  
        self,  
        csv_file_path: str,  
        config: str,  
        schema_json: str,  
        writer_type: str = "networkx"  
    ) -> Dict[str, Any]:  
        """Generate NetworkX graph using AtomSpace Builder API."""  
          
        try:  
            # Prepare files and form data  
            with open(csv_file_path, 'rb') as f:  
                files = {'files': f}  
                data = {  
                    'config': config,     
                    'schema_json': schema_json,     
                    'writer_type': writer_type     
                }  
                  
                async with httpx.AsyncClient(timeout=self.timeout) as client:  
                    # FIXED: Use client.post instead of httpx.post  
                    response = await client.post(  
                        f"{self.atomspace_url}/api/load",  
                        files=files,  
                        data=data  
                    )  
                      
                    if response.status_code != 200:  
                        raise Exception(f"AtomSpace API error: {response.status_code} - {response.text}")  
                      
                    result = response.json()  
                      
                    # NetworkX file path in shared volume  
                    networkx_file = f"/shared/output/{result['job_id']}/networkx_graph.pkl"  
                      
                    return {  
                        "job_id": result['job_id'],  
                        "networkx_file": networkx_file  
                    }  
                      
        except Exception as e:  
            raise e  
              
    async def _mine_motifs(self, networkx_file_path: str) -> Dict[str, Any]:  
        """Mine motifs using Neural Miner service."""  
        return await self.miner_service.mine_motifs(networkx_file_path)