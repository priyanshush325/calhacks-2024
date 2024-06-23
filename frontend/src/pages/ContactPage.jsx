import "../App.css";
import ContactForm from "../components/ContactForm";

const ContactPage = () => {
    return (
        <>
            <div className="flex flex-col items-center justify-center min-h-screen p-8">
                <h1 className="text-3xl font-bold mb-4">Contact Priyanshu (me)</h1>
                <ContactForm />
            </div>
        </>
    );
};

export default ContactPage;
