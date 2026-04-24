import io
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field
from project_gen.generator import generate_project
from jinja2 import Environment, FileSystemLoader

app = FastAPI(title="Project Generator API")

class ProjectOptions(BaseModel):
    platform: str = Field(..., example="Web")
    category: str = Field(..., example="E-commerce")
    colors: list[str] = Field(default_factory=lambda: ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"])
    style: str = Field(default="Modern", example="Modern")
    scope: str = Field(default="Scalable app", example="Scalable app")
    project_name: Optional[str] = Field(default=None, example="my-project")

env = Environment(loader=FileSystemLoader(Path(__file__).parent / "web_templates"))

@app.get("/", response_class=HTMLResponse)
async def web_form(request: Request):
    template = env.get_template("form.html")
    return template.render()

@app.post("/generate")
async def generate_via_api(options: ProjectOptions):
    """Generate project and return as ZIP file"""
    project_name = options.project_name or "my-project"
    opts_dict = options.dict()
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        target = tmp_dir / project_name
        generate_project(opts_dict, project_name=project_name, target_dir=target)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in target.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(tmp_dir)
                    zf.write(file_path, arcname)
        zip_buffer.seek(0)
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={project_name}.zip"}
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

@app.post("/generate-form")
async def generate_via_form(
    platform: str = Form(...),
    category: str = Form(...),
    colors: str = Form(default="#3B82F6,#10B981,#F59E0B,#EF4444,#8B5CF6"),
    style: str = Form(default="Modern"),
    scope: str = Form(default="Scalable app"),
    project_name: Optional[str] = Form(default="my-project"),
):
    """Generate project from web form and return as ZIP"""
    colors_list = [c.strip() for c in colors.split(",") if c.strip()][:5]
    options = {
        "platform": platform,
        "category": category,
        "colors": colors_list,
        "style": style,
        "scope": scope,
    }
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        target = tmp_dir / project_name
        generate_project(options, project_name=project_name, target_dir=target)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in target.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(tmp_dir)
                    zf.write(file_path, arcname)
        zip_buffer.seek(0)
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={project_name}.zip"}
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

def main():
    import uvicorn
    print("\n🚀 Project Generator Server")
    print("Web UI: http://localhost:8000")
    print("API:    http://localhost:8000/generate\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)