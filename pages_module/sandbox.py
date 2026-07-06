"""
Code Sandbox page — compiles and runs multiple languages locally
"""
import streamlit as st
import subprocess
import os
import sys
import tempfile
from utils.styles import inject_css

def run_python_code(code_str):
    import io
    import sys
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = io.StringIO()
    redirected_error = io.StringIO()
    sys.stdout = redirected_output
    sys.stderr = redirected_error
    try:
        exec(code_str, {"__builtins__": __builtins__}, {})
        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        return stdout, stderr, 0
    except Exception as e:
        import traceback
        stderr = traceback.format_exc()
        return redirected_output.getvalue(), stderr, 1
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def run_cpp_code(code_str):
    temp_dir = tempfile.gettempdir()
    cpp_filepath = os.path.join(temp_dir, "temp_sandbox.cpp")
    exe_filepath = os.path.join(temp_dir, "temp_sandbox.exe" if sys.platform == "win32" else "temp_sandbox")
    with open(cpp_filepath, "w", encoding="utf-8") as f:
        f.write(code_str)
    try:
        subprocess.run(["g++", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "", "Error: g++ compiler not found on this system.", 1
    compile_res = subprocess.run(["g++", "-O2", cpp_filepath, "-o", exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if compile_res.returncode != 0:
        if os.path.exists(cpp_filepath):
            os.remove(cpp_filepath)
        return "", f"Compilation Error:\n{compile_res.stderr}", compile_res.returncode
    try:
        run_res = subprocess.run([exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return run_res.stdout, run_res.stderr, run_res.returncode
    except subprocess.TimeoutExpired:
        return "", "Error: Execution timed out (Limit 5s).", 1
    finally:
        for path in [cpp_filepath, exe_filepath]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

def run_java_code(code_str):
    temp_dir = tempfile.gettempdir()
    java_filepath = os.path.join(temp_dir, "Main.java")
    class_filepath = os.path.join(temp_dir, "Main.class")
    with open(java_filepath, "w", encoding="utf-8") as f:
        f.write(code_str)
    try:
        subprocess.run(["javac", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "", "Error: javac (Java compiler) not found on this system.", 1
    compile_res = subprocess.run(["javac", "-d", temp_dir, java_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if compile_res.returncode != 0:
        if os.path.exists(java_filepath):
            os.remove(java_filepath)
        return "", f"Compilation Error:\n{compile_res.stderr}", compile_res.returncode
    try:
        run_res = subprocess.run(["java", "-cp", temp_dir, "Main"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return run_res.stdout, run_res.stderr, run_res.returncode
    except subprocess.TimeoutExpired:
        return "", "Error: Execution timed out (Limit 5s).", 1
    finally:
        for path in [java_filepath, class_filepath]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

def run_js_code(code_str):
    temp_dir = tempfile.gettempdir()
    js_filepath = os.path.join(temp_dir, "temp_sandbox.js")
    with open(js_filepath, "w", encoding="utf-8") as f:
        f.write(code_str)
    try:
        run_res = subprocess.run(["node", js_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return run_res.stdout, run_res.stderr, run_res.returncode
    except FileNotFoundError:
        return "", "Error: Node.js (node) is not installed on this system.", 1
    except subprocess.TimeoutExpired:
        return "", "Error: Execution timed out (Limit 5s).", 1
    finally:
        if os.path.exists(js_filepath):
            os.remove(js_filepath)

def run_typescript_code(code_str):
    temp_dir = tempfile.gettempdir()
    ts_filepath = os.path.join(temp_dir, "temp_sandbox.ts")
    js_filepath = os.path.join(temp_dir, "temp_sandbox.js")
    with open(ts_filepath, "w", encoding="utf-8") as f:
        f.write(code_str)
    try:
        subprocess.run(["tsc", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "", "Error: TypeScript compiler (tsc) not found on this system.", 1
    compile_res = subprocess.run(["tsc", ts_filepath, "--outDir", temp_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if compile_res.returncode != 0:
        if os.path.exists(ts_filepath):
            os.remove(ts_filepath)
        return "", f"Compilation Error:\n{compile_res.stderr}", compile_res.returncode
    try:
        run_res = subprocess.run(["node", js_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return run_res.stdout, run_res.stderr, run_res.returncode
    except FileNotFoundError:
        return "", "Error: Node.js (node) is not installed on this system.", 1
    except subprocess.TimeoutExpired:
        return "", "Error: Execution timed out (Limit 5s).", 1
    finally:
        for path in [ts_filepath, js_filepath]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

def run_go_code(code_str):
    temp_dir = tempfile.gettempdir()
    go_filepath = os.path.join(temp_dir, "temp_sandbox.go")
    with open(go_filepath, "w", encoding="utf-8") as f:
        f.write(code_str)
    try:
        subprocess.run(["go", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "", "Error: Go compiler not found on this system.", 1
    try:
        run_res = subprocess.run(["go", "run", go_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return run_res.stdout, run_res.stderr, run_res.returncode
    except subprocess.TimeoutExpired:
        return "", "Error: Execution timed out (Limit 5s).", 1
    finally:
        if os.path.exists(go_filepath):
            try:
                os.remove(go_filepath)
            except Exception:
                pass

def run_rust_code(code_str):
    temp_dir = tempfile.gettempdir()
    rust_filepath = os.path.join(temp_dir, "temp_sandbox.rs")
    exe_filepath = os.path.join(temp_dir, "temp_sandbox.exe" if sys.platform == "win32" else "temp_sandbox")
    with open(rust_filepath, "w", encoding="utf-8") as f:
        f.write(code_str)
    try:
        subprocess.run(["rustc", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "", "Error: Rust compiler (rustc) not found on this system.", 1
    compile_res = subprocess.run(["rustc", rust_filepath, "-o", exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if compile_res.returncode != 0:
        if os.path.exists(rust_filepath):
            os.remove(rust_filepath)
        return "", f"Compilation Error:\n{compile_res.stderr}", compile_res.returncode
    try:
        run_res = subprocess.run([exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return run_res.stdout, run_res.stderr, run_res.returncode
    except subprocess.TimeoutExpired:
        return "", "Error: Execution timed out (Limit 5s).", 1
    finally:
        for path in [rust_filepath, exe_filepath]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

def run_php_code(code_str):
    temp_dir = tempfile.gettempdir()
    php_filepath = os.path.join(temp_dir, "temp_sandbox.php")
    with open(php_filepath, "w", encoding="utf-8") as f:
        f.write(code_str)
    try:
        subprocess.run(["php", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "", "Error: PHP not found on this system.", 1
    try:
        run_res = subprocess.run(["php", php_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return run_res.stdout, run_res.stderr, run_res.returncode
    except subprocess.TimeoutExpired:
        return "", "Error: Execution timed out (Limit 5s).", 1
    finally:
        if os.path.exists(php_filepath):
            try:
                os.remove(php_filepath)
            except Exception:
                pass

def run_csharp_code(code_str):
    temp_dir = tempfile.gettempdir()
    cs_filepath = os.path.join(temp_dir, "Program.cs")
    csproj_content = '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
</Project>'''
    csproj_filepath = os.path.join(temp_dir, "temp_sandbox.csproj")
    with open(cs_filepath, "w", encoding="utf-8") as f:
        f.write(code_str)
    with open(csproj_filepath, "w", encoding="utf-8") as f:
        f.write(csproj_content)
    try:
        subprocess.run(["dotnet", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "", "Error: .NET SDK (dotnet) not found on this system.", 1
    try:
        run_res = subprocess.run(["dotnet", "run", "--project", csproj_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
        return run_res.stdout, run_res.stderr, run_res.returncode
    except subprocess.TimeoutExpired:
        return "", "Error: Execution timed out (Limit 10s).", 1
    finally:
        for path in [cs_filepath, csproj_filepath]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

def show_sandbox():
    inject_css()
    st.markdown("""
    <h1>💻 Code Sandbox</h1>
    <p style="color:#94a3b8">Write, compile and execute multiple programming languages locally.</p>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        lang = st.selectbox("Select Language", ["Python", "C++", "Java", "JavaScript", "TypeScript", "Go", "Rust", "PHP", "C#"])
        templates = {
            "Python": 'def greet(name):\n    print(f"Hello, {name} from Python!")\n\ngreet("FAANG Candidate")\n',
            "C++": '#include <iostream>\n\nint main() {\n    std::cout << "Hello from compiled C++!" << std::endl;\n    return 0;\n}\n',
            "Java": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello from Java!");\n    }\n}',
            "JavaScript": 'function greet(name) {\n    console.log("Hello, " + name + " from JavaScript!");\n}\n\ngreet("FAANG Candidate");\n',
            "TypeScript": 'function greet(name: string): void {\n    console.log("Hello, " + name + " from TypeScript!");\n}\n\ngreet("FAANG Candidate");',
            "Go": 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello from Go!")\n}',
            "Rust": 'fn main() {\n    println!("Hello from Rust!");\n}',
            "PHP": '<?php\nfunction greet($name) {\n    echo "Hello, $name from PHP!";\n}\n\ngreet("FAANG Candidate");\n?>',
            "C#": 'Console.WriteLine("Hello from C#!");'
        }
        code_key = f"sandbox_code_{lang}"
        if code_key not in st.session_state:
            st.session_state[code_key] = templates[lang]
        code = st.text_area("Source Code", value=st.session_state[code_key], height=320, key=f"editor_{lang}")
        st.session_state[code_key] = code
        if st.button("🚀 Run Code", use_container_width=True):
            with st.spinner("Running code..."):
                if lang == "Python":
                    stdout, stderr, code = run_python_code(code)
                elif lang == "C++":
                    stdout, stderr, code = run_cpp_code(code)
                elif lang == "Java":
                    stdout, stderr, code = run_java_code(code)
                elif lang == "JavaScript":
                    stdout, stderr, code = run_js_code(code)
                elif lang == "TypeScript":
                    stdout, stderr, code = run_typescript_code(code)
                elif lang == "Go":
                    stdout, stderr, code = run_go_code(code)
                elif lang == "Rust":
                    stdout, stderr, code = run_rust_code(code)
                elif lang == "PHP":
                    stdout, stderr, code = run_php_code(code)
                elif lang == "C#":
                    stdout, stderr, code = run_csharp_code(code)
            st.session_state[f"sandbox_out_{lang}"] = (stdout, stderr, code)
            
    with col2:
        st.markdown("### 🖥️ Execution Console")
        
        out_key = f"sandbox_out_{lang}"
        if out_key in st.session_state:
            stdout, stderr, exit_code = st.session_state[out_key]
            
            # Draw console background
            if exit_code == 0:
                border_color = "#10b981" # Green
                status_lbl = "SUCCESS"
            else:
                border_color = "#ef4444" # Red
                status_lbl = "FAILED"
                
            st.markdown(f"""
            <div style="font-family:var(--mono); background:#0a0e1a; border:2px solid {border_color}; border-radius:12px; padding:15px; min-height:360px;">
              <div style="display:flex; justify-content:space-between; border-bottom:1px solid #1e2d52; pb:5px; margin-bottom:10px;">
                <span style="color:#94a3b8; font-size:0.75rem;">Status: <strong style="color:{border_color};">{status_lbl}</strong></span>
                <span style="color:#94a3b8; font-size:0.75rem;">Exit Code: {exit_code}</span>
              </div>
              <div style="white-space:pre-wrap; font-size:0.85rem; color:#f1f5f9; max-height:280px; overflow-y:auto;">{stdout if stdout else ''}{f'<span style="color:#f87171;">{stderr}</span>' if stderr else ''}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Write code and click 'Run Code' to see console logs.")
