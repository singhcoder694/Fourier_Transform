import { useState } from 'react'
import './App.css'

function App() {
  const [imageData, setImage]=useState(null);
  // Function called on clicking button
  const handleClick=async ()=>{
    const send={
      text: "hello",
    }
    // fetching data from backend using Post Method.
    const response = await fetch(
      `http://localhost:8000/plot`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(send),
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    // Since data is in png format so  we are converting it to Blob and then reading the blob as DataURL.
    const blobData = await response.blob();

    // Syntax to create blobData to url which can be used in image tag
    const imageUrl = URL.createObjectURL(blobData);
    setImage(imageUrl)
  }
  return (
    <>
      {/* <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p> */}
      {imageData ? <img className='image_css' src={imageData} alt="Generated Image" /> : null}
      <button onClick={handleClick}>Click Me</button>
    </>
  )
}

export default App
