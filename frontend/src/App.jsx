import { Link, Route, BrowserRouter as Router, Routes } from "react-router-dom";
import ContactPage from "./pages/ContactPage";
import HomePage from "./pages/HomePage";
import ProjectsPage from "./pages/ProjectsPage";
function App() {
    return (
        <Router>
            <div className="bg-blue-500 text-white py-4 px-8 flex justify-between items-center">
                <div className="text-xl font-bold">Priyanshu Sharma's Personal Website</div>
                <div>
                    <Link to="/" className="ml-4">
                        Home
                    </Link>
                    <Link to="/projects" className="ml-4">
                        Projects
                    </Link>
                    <Link to="/contact" className="ml-4">
                        Contact
                    </Link>
                </div>
            </div>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/projects" element={<ProjectsPage />} />
                <Route path="/contact" element={<ContactPage />} />
            </Routes>
        </Router>
    );
}

export default App;
