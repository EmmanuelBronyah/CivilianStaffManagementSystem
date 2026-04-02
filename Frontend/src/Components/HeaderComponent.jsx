import { useEffect, useState } from "react";
import style from "../styles/components/headercomponent.module.css";
import { MdSearch, MdFilterAlt, MdDehaze } from "react-icons/md";
import image from "../assets/images/default.png";
import ThemeToggle from "./ThemeToggleComponent";
import { useTheme } from "../context/ThemeContext";
import BaseSkeleton from "./SkeletonComponent";
import api from "../api";
import { USER_ID } from "../constants";

export default function Header(props) {
  const [userInfo, setUserInfo] = useState(null);
  const [loadingUserInfo, setLoadingUserInfo] = useState(true);
  const [displayFilterBox, setDisplayFilterBox] = useState(false);
  const [placeholderText, setPlaceholderText] = useState("Service Number...");
  const { theme } = useTheme();

  useEffect(() => {
    getUserInfo();
  }, []);

  const setPlaceholder = (e) => {
    const text = e.target.textContent;
    switch (text) {
      case "Service Number":
        setPlaceholderText("Service Number...");
        setDisplayFilterBox(false);
        break;
      case "Name":
        setPlaceholderText("Name...");
        setDisplayFilterBox(false);
        break;
    }
  };

  const getUserInfo = async () => {
    try {
      const userId = localStorage.getItem(USER_ID);
      const res = await api.get(`/api/users/${userId}/`);

      setUserInfo(res.data);
      setLoadingUserInfo(false);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <header className={!theme ? style.dark : ""}>
      {/* <MobileScreenSideBar /> */}
      <MdDehaze className={style.icon} onClick={props.toggleSidebar} />
      <div className={style.activePageContainer}>
        <p>{props.activePage}</p>
      </div>
      <div className={style.searchBoxContainer}>
        <div className={style.searchBox}>
          <input type="text" placeholder={placeholderText} />
          <MdSearch className={style.searchIcon} />
          <MdFilterAlt
            className={style.filterIcon}
            onClick={() => setDisplayFilterBox((prevState) => !prevState)}
          />
          <div
            className={`${style.filterContainer} ${!displayFilterBox && style.displayNone}`}
          >
            <div className={style.text}>
              <p>Search By: </p>
            </div>
            <div className={style.filterContainerButtons}>
              <div className={style.serviceNumberButtonContainer}>
                <button onClick={setPlaceholder}>Service Number</button>
              </div>
              <div className={style.nameButtonContainer}>
                <button onClick={setPlaceholder}>Name</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <ThemeToggle className={style.switch} />
      <div className={style.profileContainer}>
        <div className={style.defaultUserImage}>
          {loadingUserInfo ? (
            <BaseSkeleton width={40} height={40} />
          ) : (
            <img
              width="40px"
              height="40px"
              src={image}
              alt="Default User Image"
            />
          )}
        </div>
        <div className={style.userNameRoleContainer}>
          {loadingUserInfo ? (
            <BaseSkeleton width={80} height={40} />
          ) : (
            <>
              <div className={style.username}>
                <p>{userInfo?.username}</p>
              </div>
              <div className={style.role}>
                <p>{userInfo?.role}</p>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
