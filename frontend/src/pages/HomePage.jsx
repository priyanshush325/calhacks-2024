import { useEffect, useState } from "react";
import img from "../assets/IMG_9407.jpg.jpeg";
const texts = ["creator", "innovator", "cool guy", "indian man", "lebron"];
const HomePage = () => {
    const [text, setText] = useState(`I am a ${texts[0]}`);

    useEffect(() => {
        const interval = setInterval(() => {
            setText((prevText) => {
                const currentIndex = texts.indexOf(prevText.slice(7)); // Removing 'I am a ' to get the original text
                const nextIndex = (currentIndex + 1) % texts.length;
                return `I am a ${texts[nextIndex]}`;
            });
        }, 2000);
        return () => clearInterval(interval);
    }, []);
    return (
        <div className="flex items-center justify-center h-screen">
            <img src={img} alt="Home" className="rounded-full w-80 h-80 object-cover" />
            <div className="ml-8">
                <div className="text-blue-500 text-4xl font-bold text-left">Hi! I'm Priyanshu Sharma!</div>
                <div className="text-blue-500 text-4xl font-bold text-left mt-4">{text}</div>
            </div>
        </div>
    );
};

export default HomePage;
