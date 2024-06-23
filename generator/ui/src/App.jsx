import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

const baseUrl = import.meta.env.VITE_PROJECT_URL;

function App() {
	const [url, setUrl] = useState(baseUrl);

	const [urlBar, setUrlBar] = useState(baseUrl);

	const [message, setMessage] = useState("");

	return (
		<>
			<div className="page">
				<div>
					<form
						onSubmit={(e) => {
							e.preventDefault();
							setUrl(urlBar);
						}}
					>
						<input
							className="url-bar"
							type="text"
							value={urlBar}
							onChange={(e) => setUrlBar(e.target.value)}
						/>
					</form>
				</div>
				<div className="content">
					<iframe
						src={url}
						title="iframe"
						// width="100%"
						id="iframe"
					></iframe>
					<div className="chat">
						<form
							onSubmit={(e) => {
								e.preventDefault();
								console.log(message);
							}}
						>
							<textarea
								className="message-box"
								type="text"
								placeholder="Type a message"
								value={message}
								onChange={(e) => setMessage(e.target.value)}
							/>
						</form>
					</div>
				</div>
			</div>
		</>
	);
}

export default App;
