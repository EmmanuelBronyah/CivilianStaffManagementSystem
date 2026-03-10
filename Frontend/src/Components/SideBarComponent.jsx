import style from "../styles/components/sidebarcomponent.module.css";
import {
  MdDashboard,
  MdAccountBox,
  MdBadge,
  MdDynamicFeed,
  MdFlag,
  MdSettings,
} from "react-icons/md";
import SidebarButtons from "./SideBarButtonsComponent";

export default function SideBar({ className, activePage, setActivePage }) {
  return (
    <aside className={className}>
      <div className={style.logoContainer}>
        <span>
          <MdBadge className={style.logo} />
        </span>
        <p>CiviBase</p>
      </div>
      <nav>
        <ul>
          <SidebarButtons
            activePage={activePage}
            setActivePage={setActivePage}
          />
        </ul>
      </nav>
    </aside>
  );
}
