import { useNavigate } from "react-router-dom";
import Header from "../Components/HeaderComponent";
import SideBar from "../Components/SideBarComponent";

function Dashboard() {
  const navigate = useNavigate();

  const navigateToLogoutPage = () => {
    navigate("/auth/logout");
  };

  return (
    <>
      <Header />
      <SideBar />
      {/* <button onClick={navigateToLogoutPage}>Logout</button> */}
    </>
  );
}

export default Dashboard;
