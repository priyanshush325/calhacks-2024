import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import peopleIcon from "./assets/people-icon.svg";
import Auth from "./components/Auth.jsx";
import DashboardPage from "./components/DashboardPage.jsx";
import "./index.css";
import Calculator from "./components/Calculator.jsx";

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
            </Routes>
            // <img src={peopleIcon} alt="People Icon" className="h-12 w-12 md:h-16 md:w-16" />
        </Router>
    );
}

export default App;
