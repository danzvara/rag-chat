import Chat from "./components/Chat";
import InfoCard from "./components/InfoCard";
import { ToastProvider } from 'react-toast-notifications';

function App() {
  return (
    <>
    <ToastProvider>
      <InfoCard />
      <Chat />
    </ToastProvider>
    </>
  );
}

export default App;
