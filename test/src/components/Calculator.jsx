import { useEffect, useState } from "react";
import { handleCalculate } from "../utils/helpers";
import NumberButton from "./NumberButton";

const Calculator = () => {
    const [input, setInput] = useState("");

    const handleClick = (value) => {
        setInput(input + value);
    };

    const calculate = () => {
        try {
            setInput(String(handleCalculate(input)));
        } catch (error) {
            setInput("Error");
        }
    };

    const clearInput = () => {
        setInput("");
    };

    const handleKeydown = (event) => {
        switch (event.key) {
            case "Enter":
                calculate();
                break;
            case "Escape":
                clearInput();
                break;
            case "+":
            case "-":
            case "*":
            case "/":
            case ".":
            case "0":
            case "1":
            case "2":
            case "3":
            case "4":
            case "5":
            case "6":
            case "7":
            case "8":
            case "9":
                handleClick(event.key);
                break;
            default:
                break;
        }
    };

    useEffect(() => {
        window.addEventListener("keydown", handleKeydown);
        return () => {
            window.removeEventListener("keydown", handleKeydown);
        };
    }, [input]);

    return (
        <div className="flex justify-center items-center min-h-screen bg-gray-100">
            <div className="bg-white p-5 rounded-lg shadow-md">
                <input
                    type="text"
                    value={input}
                    readOnly
                    className="w-full p-2 mb-3 text-right bg-gray-200 rounded-lg"
                />
                <div className="grid grid-cols-4 gap-3">
                    {["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "=", "+"].map((symbol) => (
                        <NumberButton
                            key={symbol}
                            value={symbol}
                            onClick={() => (symbol === "=" ? calculate() : handleClick(symbol))}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Calculator;
