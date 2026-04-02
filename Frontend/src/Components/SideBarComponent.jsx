import style from "../styles/components/sidebarcomponent.module.css";
import { MdBadge, MdClose } from "react-icons/md";
import SidebarButtons from "./SideBarButtonsComponent";
import { useTheme } from "../context/ThemeContext";

export default function SideBar(props) {
  const { theme } = useTheme();
  return (
    <aside
      className={`${!theme ? style.dark : ""} ${props.displaySidebar ? style.sideBarMobile : ""}`}
    >
      <div className={style.logoContainer}>
        <span>
          <MdBadge className={style.logo} />
        </span>
        <p>CiviBase</p>
        <MdClose
          onClick={props.toggleSidebar}
          className={`${style.closeIcon} ${style.showCloseIcon}`}
        />
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
