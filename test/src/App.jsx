import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import Auth from "./components/Auth.jsx";
import Calculator from "./components/Calculator.jsx";
import DashboardPage from "./components/DashboardPage.jsx";
import "./index.css";
import PlaygroundPage from "./pages/PlaygroundPage.jsx";

import ProfilePage from "./components/ProfilePage.jsx";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Auth />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/auth" element={<Auth />} />
                <Route path="/calculator" element={<Calculator />} />
                <Route path="/playground" element={<PlaygroundPage />} />
            </Routes>
        </Router>
    );
}

export default App;
