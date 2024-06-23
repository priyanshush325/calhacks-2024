import { useEffect, useRef, useState } from "react";
import TextareaAutosize from "react-textarea-autosize";
import "./App.css";

const baseUrl = import.meta.env.VITE_PROJECT_URL;
const serverUrl = import.meta.env.VITE_SERVER_URL;

const DEFAULT_PROJECT_PATH =
	"/Users/sonavagarwal/Documents/GitHub/calhacks-2024/health_app";

async function sendMessage(message) {
	let response = await fetch(serverUrl + "/prompt", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			prompt: message,
		}),
	});

	let data = null;
	if (response.status === 200) {
		data = await response.json();
		console.log(data);
	}

	return {
		success: response.status === 200,
		data: data,
	};
}

async function confirmActions(confirm) {
	let response = await fetch(serverUrl + "/confirm", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			confirm: confirm,
		}),
	});

	return response.status === 200;
}

async function sendProject(project) {
	console.log(project);
	let response = await fetch(serverUrl + "/info", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			// projectName: project.name,
			projectSourceDir: project.path,
		}),
	});

	console.log(response);

	return response.status === 200;
}

function App() {
	const [project, setProject] = useState({
		name: "It literally doesn't matter",
		path: DEFAULT_PROJECT_PATH,
	});
	const [projectSet, setProjectSet] = useState(false);

	const [url, setUrl] = useState(baseUrl);
	const [urlBar, setUrlBar] = useState(baseUrl);

	const [message, setMessage] = useState("");
	const [awaitingConfirmation, setAwaitingConfirmation] = useState(false);

	const [currentStatus, setCurrentStatus] = useState("");
	const [inputEnabled, setInputEnabled] = useState(false);
	const inputRef = useRef(null);
	useEffect(() => {
		if (inputEnabled) {
			inputRef.current.focus();
		}
	}, [inputEnabled]);
	const [actionPlan, setActionPlan] = useState({
		actions: [],
		commands: [],
	});
	// each action has action, filePath, prompt, and contextFiles []

	return (
		<>
			<div className="page">
				<div className="content">
					<div>
						<form
							className="url-bar-container"
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
							<button
								onClick={() => {
									let random = Math.floor(Math.random() * 1000000);
									setUrl(urlBar + "?random=" + random);
								}}
								className="reload-button"
							>
								Reload
							</button>
						</form>
					</div>
					<div className="iframe-container">
						{projectSet && (
							<iframe
								src={url}
								title="iframe"
								// width="100%"
								id="iframe"
							></iframe>
						)}
						{!projectSet && (
							<div className="chat-settings">
								<h1>Select a Project</h1>
								{/* <input
									type="text"
									placeholder="Project name"
									onChange={(e) =>
										setProject({ ...project, name: e.target.value })
									}
								/> */}
								<input
									type="text"
									placeholder="Absolute project path"
									defaultValue={DEFAULT_PROJECT_PATH}
									onChange={(e) =>
										setProject({ ...project, path: e.target.value })
									}
								/>
								<button
									onClick={async () => {
										if (project.path === "") {
											alert("Please enter a project path");
											return;
										}
										setCurrentStatus("Loading project");
										let successs = await sendProject(project);
										if (successs) {
											setCurrentStatus("Waiting for messages");
											setProjectSet(true);
											setInputEnabled(true);
											setTimeout(() => {
												// reload the iframe
												setUrl(
													urlBar +
														"?random=" +
														Math.floor(Math.random() * 1000000)
												);
											}, 1000);
										}
									}}
									onKeyDown={(e) => {
										if (e.key === "Enter") {
											if (project.path === "") {
												alert("Please enter a project path");
												return;
											}
										}
									}}
								>
									Submit
								</button>
							</div>
						)}
					</div>
				</div>
				<div className="chat">
					<div
						style={{
							flex: 1,
							display: "flex",
							flexDirection: "column",
							gap: "0.5rem",
						}}
					>
						{!!currentStatus && <h1 className="status">{currentStatus}</h1>}

						{actionPlan?.commands?.map((command, index) => (
							<div key={index} className="command">
								Run {command}
							</div>
						))}
						{actionPlan?.actions?.map((action, index) => (
							<div key={index} className="action">
								<div className="action-action">
									{action.action}{" "}
									<span className="action-file">{action.filePath}</span>
								</div>
								<div className="action-prompt">{action.prompt}</div>
								<ul className="action-context">
									{action.contextFiles.length > 0 && "Context files:"}
									{action.contextFiles.map((contextFile, index) => (
										<li key={index} className="context-file">
											{contextFile}
										</li>
									))}
									{action.contextFiles.length === 0 && "No context files"}
								</ul>
							</div>
						))}
					</div>

					<TextareaAutosize
						ref={inputRef}
						disabled={!inputEnabled}
						className="message-box"
						type="text"
						placeholder={
							awaitingConfirmation
								? "Enter to confirm, anything else to cancel..."
								: "Enter a prompt..."
						}
						style={{
							opacity: inputEnabled ? 1 : 0.5,
							cursor: inputEnabled ? "auto" : "not-allowed",
						}}
						value={message}
						onChange={(e) => setMessage(e.target.value)}
						onKeyDown={async (e) => {
							if (e.key === "Enter") {
								e.preventDefault();

								console.log("Enter pressed");

								if (awaitingConfirmation) {
									setInputEnabled(false);
									if (message === "") {
										setCurrentStatus("Executing plan");
										const success = await confirmActions(true);
										setAwaitingConfirmation(false);
										setMessage("");
										if (success) {
											setActionPlan({
												actions: [],
												commands: [],
											});
										}
									} else {
										setCurrentStatus("Cancelling plan");
										const success = await confirmActions(false);
										setAwaitingConfirmation(false);
										setMessage("");
										if (success) {
											setActionPlan({
												actions: [],
												commands: [],
											});
										}
									}
									setTimeout(() => {
										setCurrentStatus("");
										setInputEnabled(true);
									}, 100);
								} else {
									console.log("Sending message", message);
									if (message === "") return;
									setCurrentStatus("Sending message");
									let messageSave = message;
									setMessage("");
									setInputEnabled(false);
									const result = await sendMessage(messageSave);
									if (result.success) {
										if (
											result.data?.actions?.length === 0 &&
											result.data?.commands?.length === 0
										) {
											setCurrentStatus("No actions required");
											setTimeout(() => {
												setCurrentStatus("");
												setInputEnabled(true);
											}, 1000);
											return;
										} else {
											setAwaitingConfirmation(true);
											setActionPlan(result.data);
											setTimeout(() => {
												setCurrentStatus("Awaiting confirmation");
												setInputEnabled(true);
											}, 100);
										}
									} else {
										alert("Error sending message");
										setCurrentStatus("");
										setInputEnabled(true);
									}
								}
							}
						}}
					/>
				</div>
			</div>
		</>
	);
}

export default App;
