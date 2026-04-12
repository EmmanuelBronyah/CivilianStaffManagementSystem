import { useState } from "react";
import AddUsersComponent from "./AddUsersComponent";
import AllUsersComponent from "./AllUsersComponent";
import style from "../../../styles/components/userscomponent.module.css";
import { useTheme } from "../../../Context/ThemeContext";

export default function Users() {
  const [userPage, setUserPage] = useState("Add User");
  const { theme } = useTheme();
  return (
    <main className={`${style.usersMain} ${!theme ? style.dark : ""}`}>
      {userPage === "All Users" && (
        <AllUsersComponent setUserPage={setUserPage} />
      )}
      {userPage === "Add User" && (
        <AddUsersComponent setUserPage={setUserPage} />
      )}
    </main>
  );
}
