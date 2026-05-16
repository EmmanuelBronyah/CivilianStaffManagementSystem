import {
  MdDashboard,
  MdAccountBox,
  MdBadge,
  MdDynamicFeed,
  MdFlag,
  MdSettings,
} from "react-icons/md";
import style from "../../styles/components/sidebarcomponent.module.css";
import { NavLink } from "react-router-dom";
import useFetchUserRole from "../../Features/hooks/fetchUserRoleHook";
import { useEffect } from "react";

export default function SidebarButtons(props) {
  const { role, response } = useFetchUserRole();

  useEffect(() => {
    if (!response) return;
    props.setResponse(response);
  });

  useEffect(() => {
    if (!response) return;
    props.setResponse(response);
  });

  const buttonInfo = [
    ["Dashboard", MdDashboard, "/home"],
    ["Users", MdAccountBox, "/home/users"],
    ["Employees", MdBadge, "/home/employees"],
    ["Activity Feeds", MdDynamicFeed, "/home/feeds"],
    ["Flags", MdFlag, "/home/flags"],
    ["Settings", MdSettings, "/home/settings"],
  ];

  const buttons = buttonInfo.map(([text, icon, route]) => {
    const Icon = icon;
    const isDashboard = route === "/home";
    return (
      <li key={text}>
        <NavLink
          to={route}
          className={({ isActive }) => (isActive ? style.active : "")}
          end={isDashboard}
        >
          <button>
            <span>
              <Icon className={style.icon} />
            </span>
            <p>{text}</p>
          </button>
        </NavLink>
      </li>
    );
  });

  console.log(buttons);

  return buttons;
}
