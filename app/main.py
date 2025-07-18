from fastapi import FastAPI

app = FastAPI(title="Miniature EC Backend", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello from miniature-ec-backend!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

def main():
    print("Hello from miniature-ec-backend!")

if __name__ == "__main__":
    main()
