
import inspect
from integration_service.services.orchestration_service import OrchestrationService
from integration_service.api.pipeline import execute_pipeline

print("OrchestrationService._generate_networkx signature:")
print(inspect.signature(OrchestrationService._generate_networkx))

print("\nChecking for 'files' argument in _generate_networkx...")
sig = inspect.signature(OrchestrationService._generate_networkx)
if 'files' in sig.parameters:
    print("FOUND 'files' argument!")
else:
    print("Did NOT find 'files' argument.")

# I can't easily inspect the body of execute_pipeline to see the call arguments without parsing AST,
# but I can check if the file on disk contains 'files='
with open('integration_service/api/pipeline.py', 'r') as f:
    content = f.read()
    if 'files=' in content:
        print("\nFound 'files=' in integration_service/api/pipeline.py")
        for line in content.splitlines():
            if 'files=' in line:
                print(f"Line: {line.strip()}")
    else:
        print("\nDid NOT find 'files=' in integration_service/api/pipeline.py")
