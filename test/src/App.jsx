import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import Auth from "./components/Auth.jsx";
import HomePage from "./components/HomePage.jsx";

import ProfilePage from "./components/ProfilePage.jsx";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/auth" element={<Auth />} />
            </Routes>
        </Router>
    );
}

export default App;
