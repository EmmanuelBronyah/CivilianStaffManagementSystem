import { useEffect, useState } from "react";
import style from "../../styles/components/headercomponent.module.css";
import { MdSearch, MdFilterAlt, MdDehaze } from "react-icons/md";
import image from "../../assets/images/default.png";
import ThemeToggle from "../../Components/Common/ThemeToggleComponent";
import { useTheme } from "../../context/ThemeContext";
import BaseSkeleton from "../Common/SkeletonComponent";
import api from "../../api";
import { USER_ID } from "../../constants";
import getResponseMessages from "../../utils/extractResponseMessage";
import { useLocation, useSearchParams } from "react-router-dom";

export default function Header(props) {
  const [userInfo, setUserInfo] = useState(null);
  const [loadingUserInfo, setLoadingUserInfo] = useState(true);
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchItem, setSearchItem] = useState(searchParams.get("q") || "");

  const location = useLocation();
  const { theme } = useTheme();

  useEffect(() => {
    const getUserInfo = async () => {
      try {
        // const userId = localStorage.getItem(USER_ID);
        const userId = 1;
        const res = await api.get(`/api/users/${userId}/`);

        setUserInfo(res.data);
        setLoadingUserInfo(false);
      } catch (error) {
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };

    getUserInfo();
  }, []);

  //   switch (text) {
  //     case "Service Number":
  //       setPlaceholderText("Service Number...");
  //       setDisplayFilterBox(false);
  //       break;
  //     case "Name":
  //       setPlaceholderText("Name...");
  //       setDisplayFilterBox(false);
  //       break;
  //   }
  // };

  const routes = [
    {
      path: "/home/users",
      title: "Users",
    },

    {
      path: "/home/employees",
      title: "Employees",
    },

    {
      path: "/home/feeds",
      title: "Activity Feeds",
    },

    {
      path: "/home/settings",
      title: "Settings",
    },

    {
      path: "/home",
      title: "Dashboard",
    },
  ];

  const activeRoute = routes.find((route) =>
    location.pathname.startsWith(route.path),
  );
  const activePage = activeRoute?.title || "Dashboard";

  return (
    <header className={!theme ? style.dark : ""}>
      <MdDehaze className={style.icon} onClick={() => props.setOpen(true)} />
      <div className={style.activePageContainer}>
        <p>{activePage}</p>
      </div>
      <div className={style.searchBoxContainer}>
        <div className={style.searchBox}>
          <input
            type="text"
            placeholder={"Search name or service number..."}
            value={searchItem}
            onChange={(e) => setSearchItem(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                setSearchParams({
                  q: searchItem,
                  page: 1,
                });
              }
            }}
          />

          <MdSearch className={style.searchIcon} />
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
