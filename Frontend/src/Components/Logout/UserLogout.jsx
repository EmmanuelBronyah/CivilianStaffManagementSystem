import { Route, useNavigate } from "react-router-dom";
import api from "../../api";
import { ACCESS_TOKEN, REFRESH_TOKEN, TEMP_TOKEN } from "../../constants";

export default function LogoutUser({ route }) {
  const navigate = useNavigate();

  const confirmLogout = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN);

    try {
      const res = await api.post(route, { refresh_token: refreshToken });
      if (res.status === 200) {
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        localStorage.removeItem(TEMP_TOKEN);
        console.log("Response: ", res.data.detail);
        setTimeout(() => {
          navigate("/auth/login/");
        }, 900);
      }
    } catch (error) {
      if (error.response) {
        console.log("Error: ", error.response.data);
      } else {
        console.log("Unexpected Error: ", error);
      }
    }
  };

  const cancelLogout = () => {
    navigate("/dashboard");
  };

  return (
    <>
      <p>Are you sure you want to logout?</p>
      <button onClick={confirmLogout}>Yes</button>
      <button onClick={cancelLogout}>No</button>
    </>
  );
}
