import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import './tailwind.css';

function App() {
    const [input, setInput] = useState("");
    const handleClick = (value) => {
        setInput(input + value);
    };
    const calculateResult = () => {
        try {
            setInput(String(eval(input)));
        } catch {
            setInput("Error");
        }
    };
    const clearInput = () => {
        setInput("");
    };
return (
    <div className="flex justify-center items-center h-screen bg-white">
        <div className="calculator p-4">
            <input
                type="text"
                value={input}
                readOnly
                className="bg-gray-200 font-bold mb-4 p-2 w-full rounded"
            />
            <div className="grid grid-cols-4 gap-2">
                {['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'].map((num) => (
                    <button
                        key={num}
                        onClick={() => handleClick(num)}
                        className="bg-gray-200 rounded p-2 w-full h-12"
                    >
                        {num}
                    </button>
                ))}
                {['+', '-', '*', '/'].map((op) => (
                    <button
                        key={op}
                        onClick={() => handleClick(op)}
                        className="bg-gray-200 rounded p-2 w-full h-12"
                    >
                        {op}
                    </button>
                ))}
                <button
                    onClick={calculateResult}
                    className="bg-orange-500 rounded p-2 w-full h-12 col-span-2"
                >=</button>
                <button
                    onClick={clearInput}
                    className="bg-gray-200 rounded p-2 w-full h-12 col-span-2"
                >C</button>
            </div>
        </div>
    </div>
);
    );
}

export default App;
