import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import HomePage from "./components/HomePage.jsx";
import ProfilePage from "./components/ProfilePage.jsx";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/profile" element={<ProfilePage />} />
            </Routes>
        </Router>
    );
}

export default App;
