import AddUsersComponent from "./AddUsersComponent";
import AllUsersComponent from "./AllUsersComponent";
import style from "../../../styles/components/userscomponent.module.css";
import { useTheme } from "../../../Context/ThemeContext";
import UpdateUser from "./UpdateUserComponent";
import { Outlet } from "react-router-dom";

export default function Users() {
  const { theme } = useTheme();

  return (
    <main className={`${style.usersMain} ${!theme ? style.dark : ""}`}>
      <Outlet />
    </main>
  );
}
