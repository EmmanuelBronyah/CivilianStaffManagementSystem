import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  const navigateToLogoutPage = () => {
    navigate("/auth/logout");
  };

  return (
    <>
      <h1>My Dashboard</h1>
      <button onClick={navigateToLogoutPage}>Logout</button>
    </>
  );
}

export default Dashboard;
