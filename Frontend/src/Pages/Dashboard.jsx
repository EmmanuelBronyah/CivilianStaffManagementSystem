import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { TEMP_TOKEN } from "../constants";
import Header from "../Components/HeaderComponent";
import SideBar from "../Components/SideBarComponent";

function Dashboard() {
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem(TEMP_TOKEN);
  }, []);

  const navigateToLogoutPage = () => {
    navigate("/auth/logout");
  };

  return (
    <>
      <Header />
      <SideBar />
      <button onClick={navigateToLogoutPage}>Logout</button>
    </>
  );
}

export default Dashboard;
