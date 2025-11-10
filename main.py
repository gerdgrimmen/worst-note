import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

api_data = {
    "tags": {},
    "notes": {},
}

PORT = 5000

class API():
    def __init__(self):
        self.routing = { "GET": { }, "POST": { } , "DELETE": { } }
    
    def get(self, path):
        def wrapper(fn):
            self.routing["GET"][path] = fn
        return wrapper

    def post(self, path):
        def wrapper(fn):
            self.routing["POST"][path] = fn
        return wrapper

    def delete(self, path):
        def wrapper(fn):
            self.routing["DELETE"][path] = fn
        return wrapper

api = API()


@api.get("/")
def index(_):
    return { 
        "name": "Rest API for simple note taking",
        "summary": "",
        "endpoints": [ "/tags", "/notes", "/help" ],
        "version": "0.1.0"
    }

@api.get("/help")
def get_help(args):
    return {"help": "help"}

@api.get("/tags")
def get_tags(args):
    if "path_id" in args.keys():
        if args["path_id"] in api_data["tags"].keys():
            return api_data["tags"][args["path_id"]]
        else:
            return {"message": "not found"}
    return {"tags": api_data["tags"]}

@api.post("/tags")
def post_tag(body):
    if not "text" in body.keys():
        return {"message": "invalid entry"}
    next_id = len(api_data["tags"].keys())
    api_data["tags"][next_id] = body["text"]
    return {"id": str(next_id)}

@api.get("/notes")
def get_notes(args):
    if "path_id" in args.keys():
        if args["path_id"] in api_data["notes"].keys():
            return api_data["notes"][args["path_id"]]
        else:
            return {"message": "not found"}
    return {"notes": api_data["notes"]}

@api.post("/notes")
def post_note(body):
    if not "text" in body.keys():
        return {"message": "invalid entry"}
    next_id = len(api_data["notes"].keys())
    api_data["notes"][next_id] = body["text"]
    return {"id": str(next_id)}

@api.delete("/notes")
def delete_note(body):
    if not "id" in body.keys():
        return {"message": "invalid am entry"}
    print(body)
    print(api_data["notes"].keys())
    if int(body["id"]) in api_data["notes"].keys():
        api_data["notes"].pop(int(body["id"]))
        print("deleting")
        return {"message": "deleted"}
    return {"message": "not found"}

if __name__ == "__main__":
    class ApiRequestHandler(BaseHTTPRequestHandler):
        global api
        
        def call_api(self, method, path, args):
            if path in api.routing[method]:
                try:
                    result = api.routing[method][path](args)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps(result, indent=4).encode())
                except Exception as e:
                    self.send_response(500, "Server Error")
                    self.end_headers()
                    self.wfile.write(json.dumps({ "error": e.args }, indent=4).encode())
            else:
                self.send_response(404, "Not Found")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "not found"}, indent=4).encode())

        def do_GET(self):
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            args = parse_qs(parsed_url.query)
            if not path in api.routing["GET"]:
                new_path, path_id = path.rsplit("/",1)
                if new_path == "": new_path = "/"
                if new_path in api.routing["GET"]: 
                    path = new_path
                    args["path_id"] = path_id
            for k in args.keys():
                if len(args[k]) == 1:
                    args[k] = args[k][0]
            
            self.call_api("GET", path, args)

        def do_POST(self):
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            if self.headers.get("content-type") != "application/json":
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "posted data must be in json format"
                }, indent=4).encode())
            else:
                data_len = int(self.headers.get("content-length"))
                data = self.rfile.read(data_len).decode()
                self.call_api("POST", path, json.loads(data))

        def do_DELETE(self):
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            if self.headers.get("content-type") != "application/json":
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "posted data must be in json format"
                }, indent=4).encode())
            else:
                data_len = int(self.headers.get("content-length"))
                data = self.rfile.read(data_len).decode()
                self.call_api("DELETE", path, json.loads(data))

    httpd = HTTPServer(('', PORT), ApiRequestHandler)
    print(f"Application started at http://127.0.0.1:{PORT}/")
    httpd.serve_forever()