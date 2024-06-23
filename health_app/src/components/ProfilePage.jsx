import { useState } from "react";
import "../App.css";
const ProfilePage = () => {
    const [user, setUser] = useState(null);

    return (
        <div className="flex justify-center items-center h-screen">
            <h1>Profile</h1>
        </div>
    );
};

export default ProfilePage;
