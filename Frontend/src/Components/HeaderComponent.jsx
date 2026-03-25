import { useEffect, useState } from "react";
import style from "../styles/components/headercomponent.module.css";
import { MdSearch, MdFilterAlt } from "react-icons/md";
import image from "../assets/images/default.png";
import ThemeToggle from "./ThemeToggleComponent";
import { useTheme } from "../context/ThemeContext";
import BaseSkeleton from "./SkeletonComponent";
import api from "../api";
import { USER_ID } from "../constants";

export default function Header(props) {
  const [userInfo, setUserInfo] = useState(null);
  const [loadingUserInfo, setLoadingUserInfo] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [hideSearchIcon, setHideSearchIcon] = useState(false);
  const { theme } = useTheme();

  useEffect(() => {
    if (searchQuery) {
      setHideSearchIcon(true);
    } else {
      setHideSearchIcon(false);
    }
  }, [searchQuery]);

  useEffect(() => {
    getUserInfo();
  }, []);

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
      <div className={style.activePageContainer}>
        <p>{props.activePage}</p>
      </div>
      <div className={style.searchBoxContainer}>
        <div className={style.searchBox}>
          <input type="text" onChange={(e) => setSearchQuery(e.target.value)} />
          <MdSearch
            className={`${style.searchIcon} ${hideSearchIcon && style.hide}`}
          />
          <MdFilterAlt className={style.filterIcon} />
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
        {loadingUserInfo ? (
          <BaseSkeleton width={80} height={40} />
        ) : (
          <div className={style.userNameRoleContainer}>
            <div className={style.username}>
              <p>{userInfo && userInfo.username}</p>
            </div>
            <div className={style.role}>
              <p>{userInfo && userInfo.role}</p>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
