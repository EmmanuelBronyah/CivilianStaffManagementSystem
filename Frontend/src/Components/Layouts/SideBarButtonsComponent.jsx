import {
  MdDashboard,
  MdAccountBox,
  MdBadge,
  MdDynamicFeed,
  MdFlag,
  MdSettings,
} from "react-icons/md";
import style from "../../styles/components/sidebarcomponent.module.css";

export default function SidebarButtons({ activePage, setActivePage }) {
  const buttonsTextAndIcon = [
    ["Dashboard", MdDashboard],
    ["Users", MdAccountBox],
    ["Employees", MdBadge],
    ["Activity Feeds", MdDynamicFeed],
    ["Flags", MdFlag],
    ["Settings", MdSettings],
  ];

  const buttons = buttonsTextAndIcon.map(([text, icon]) => {
    const Icon = icon;
    return (
      <li key={text}>
        <button
          className={activePage === text ? style.active : ""}
          onClick={() => setActivePage(text)}
        >
          <span>
            <Icon className={style.icon} />
          </span>
          <p>{text}</p>
        </button>
      </li>
    );
  });

  return buttons;
}
