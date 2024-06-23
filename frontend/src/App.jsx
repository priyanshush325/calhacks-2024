import { useState } from "react";
import "./App.css";
import CalculatorComponent from "./components/CalculatorComponent.jsx";

function App() {
    const [count, setCount] = useState(0);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen w-full">
            <CalculatorComponent />
        </div>
    );
}

export default App;
