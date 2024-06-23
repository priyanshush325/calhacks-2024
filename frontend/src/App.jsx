import { useState } from "react";
import "./App.css";
import CalculatorComponent from "./components/CalculatorComponent.jsx";

function App() {
    const [count, setCount] = useState(0);

    return (
        <div className="flex items-center justify-center min-h-screen p-4">
            <div className="calculator space-y-4 w-96">
                <div className="display bg-gray-200 p-4 text-bold text-xl h-16 flex items-center justify-end rounded">
                    {input}
                </div>
                <div className="grid grid-cols-4 gap-2">
                    {[...Array(10).keys()].map((num) => (
                        <button
                            key={num}
                            className="bg-gray-200 hover:bg-gray-300 rounded-full w-20 h-20 flex items-center justify-center"
                            onClick={() => handleButtonClick(num.toString())}
                        >
                            {num}
                        </button>
                    ))}
                    <button
                        className="bg-blue-500 hover:bg-blue-600 rounded-full w-20 h-20 flex items-center justify-center"
                        onClick={() => handleButtonClick("+")}
                    >
                        +
                    </button>
                    <button
                        className="bg-blue-500 hover:bg-blue-600 rounded-full w-20 h-20 flex items-center justify-center"
                        onClick={() => handleButtonClick("-")}
                    >
                        -
                    </button>
                    <button
                        className="bg-blue-500 hover:bg-blue-600 rounded-full w-20 h-20 flex items-center justify-center"
                        onClick={() => handleButtonClick("*")}
                    >
                        *
                    </button>
                    <button
                        className="bg-gray-500 hover:bg-gray-600 rounded-full w-20 h-20 flex items-center justify-center"
                        onClick={() => handleClear()}
                    >
                        C
                    </button>
                    <button
                        className="bg-orange-500 hover:bg-orange-600 rounded-full w-20 h-20 flex items-center justify-center"
                        onClick={() => setInput(handleCalculate(input))}
                    >
                        =
                    </button>
                </div>
            </div>
        </div>
    );
}

export default App;
