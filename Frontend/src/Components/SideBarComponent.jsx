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

export default function SideBar(props) {
  return (
    <aside>
      <div className={style.logoContainer}>
        <span>
          <MdBadge className={style.logo} />
        </span>
        <p>CiviBase</p>
      </div>
      <nav>
        <ul>
          <SidebarButtons
            activePage={props.activePage}
            setActivePage={props.setActivePage}
          />
        </ul>
      </nav>
    </aside>
  );
}
