import style from "../../styles/components/sidebarcomponent.module.css";
import { MdBadge, MdClose } from "react-icons/md";
import SidebarButtons from "../../Components/Layouts/SideBarButtonsComponent";
import { useTheme } from "../../Context/ThemeContext";
import useFetchUserRole from "../../Features/hooks/fetchUserRoleHook";
import { useEffect } from "react";
import BaseSkeleton from "../Common/SkeletonComponent";

export default function SideBar(props) {
  const { role, response } = useFetchUserRole();

  const { theme } = useTheme();

  useEffect(() => {
    if (!response) return;
    props.setResponse(response);
  });

  return (
    <aside className={!theme ? style.dark : ""} data-open={props.open}>
      <div className={style.logoContainer}>
        <span>
          <MdBadge className={style.logo} />
        </span>
        <p>CiviBase</p>
        <MdClose
          onClick={() => props.setOpen(false)}
          className={`${style.closeIcon} ${style.showCloseIcon}`}
        />
      </div>
      {!role ? (
        <BaseSkeleton height="70%" />
      ) : (
        <nav>
          <ul>
            <SidebarButtons role={role} />
          </ul>
        </nav>
      )}
    </aside>
  );
}
