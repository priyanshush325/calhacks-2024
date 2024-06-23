import img from "../assets/IMG_9407.jpg.jpeg";

const HomePage = () => {
    return (
        <div className="flex flex-col items-start justify-center h-screen p-8 text-left">
            <div className="flex items-center justify-center p-4">
                <img src={img} alt="Home" className="rounded-full w-80 h-80 object-cover animate-spin-slow" />
                <div className="ml-8 text-left">
                    <div className="text-blue-500 text-4xl font-bold">Hi! I'm Priyanshu Sharma!</div>
                    <section className="mt-4">
                        <p className="text-lg text-gray-700">
                            Hi I'm Priyanshu Sharma and I'm a passionate student studying computer science at UCLA. In
                            my free time, I like to watch LeBron James play basketball.
                        </p>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default HomePage;
