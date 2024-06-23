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
        <div className="flex flex-col items-center justify-center h-screen p-8 text-center">
            <div className="flex items-center justify-center p-4">
                <img src={img} alt="Home" className="rounded-full w-80 h-80 object-cover animate-spin-slow" />
                <div className="ml-8 text-center">
                    <div className="text-blue-500 text-4xl font-bold">Hi! I'm Priyanshu Sharma!</div>
                    <section className="mt-4">
                        <p className="text-lg text-gray-700">
                            Hi I'm Priyanshu Sharma and I'm a passionate student studying computer science at UCLA. In my
                            free time, I like to watch LeBron James play basketball and I also have a girlfriend who's an
                            opp.
                        </p>
                    </section>
                    <section className="mt-4 text-lg text-gray-700">
                        <p>{text}</p>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default HomePage;

