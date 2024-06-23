import { useState } from "react";
import "./App.css";

function App() {
    const [count, setCount] = useState(0);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen w-full">
            <h1 className="text-2xl">Hello World</h1>
        </div>
    );
}

export default App;
