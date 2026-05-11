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

export default function SidebarButtons({ activePage, setActivePage }) {
  const buttonInfo = [
    ["Dashboard", MdDashboard, "/home"],
    ["Users", MdAccountBox, "/home/users/all"],
    ["Employees", MdBadge, "/home/employees"],
    ["Activity Feeds", MdDynamicFeed, "/home/feeds"],
    ["Flags", MdFlag, "/home/flags"],
    ["Settings", MdSettings, "/home/settings"],
  ];

  const buttons = buttonInfo.map(([text, icon, route]) => {
    const Icon = icon;
    return (
      <NavLink
        to={route}
        className={({ isActive }) => (isActive ? style.active : "")}
      >
        <li key={text}>
          <button>
            <span>
              <Icon className={style.icon} />
            </span>
            <p>{text}</p>
          </button>
        </li>
      </NavLink>
    );
  });

  return buttons;
}
