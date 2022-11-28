import {
    AppBar,
    Toolbar,
    Typography,
    makeStyles,
    Button,
    IconButton,
    Drawer,
    Link,
    MenuItem,
    Paper,
    Avatar,
    Box,
    Divider
} from "@material-ui/core";
import Grid from '@material-ui/core/Grid';
import Popover from '@material-ui/core/Popover';
import MenuIcon from "@material-ui/icons/Menu";
import CloseIcon from '@material-ui/icons/Close';
import SettingsOutlinedIcon from '@material-ui/icons/SettingsOutlined';
import React, { useState, useEffect, useRef } from "react";
import { Link as RouterLink } from "react-router-dom";
import AnuvaadLogo from "../../../../assets/HeaderTransparentLogo.png";
import configs from "../../../../configs/configs";
import headerMenuConfig from "../../../../configs/headerMenuConfig";

const useStyles = makeStyles((theme) => ({
    header: {
        backgroundImage: "linear-gradient(to right, rgb(241, 241, 241), rgb(255, 255, 255))",
        paddingRight: "40px",
        paddingLeft: "40px",
        "@media (max-width: 900px)": {
            // paddingLeft: 0,
            paddingRight: 0,
            paddingLeft: 0,
        },
    },
    logo: {
        // height: "2rem",
        width: "6rem"
    },
    // ".MuiButton-label":{
    //     letterSpacing: "0.5px"
    // },

    // inactive button menu styles
    menuButton: {
        fontFamily: "roboto",
        padding: 18,
        fontWeight: 500,
        color: "#000000",
        fontSize: "19px",
        // size: "200px",
        marginLeft: "20px",
        '&:hover': {
            backgroundColor: "#E0E0E0",
            color: "#000000",
            // padding: 18,
            borderRadius: 12
        }
    },
    highlightedMenuButton: {
        fontFamily: "roboto",
        backgroundColor: "#E0E0E0",
        borderRadius: 12,
        padding: 18,
        fontWeight: 500,
        color: "#000000",
        fontSize: "19px",
        letterSpacing: "0.5px",
        // size: "18px",
        marginLeft: "20px",
        // backgroundColor: "#E0E0E0",
        // color: "#000000",
        // padding: 15,
        // borderRadius: 10,
        // fontWeight: 700,
    },
    toolbar: {
        display: "flex",
        justifyContent: "space-between",
        "@media (min-width: 900px)": {
            // paddingLeft: 0,
            paddingRight: "16.8px",
            paddingLeft: "16.8px",
        },
    },
    desktopMenuContainer: {
        display: "flex",
        justifyContent: "space-between",
    },
    drawerContainer: {
        padding: "20px 30px",
    },
    paper: {
        height: 50,
        width: 50,
    },
    control: {
        padding: theme.spacing(2),
    },
    popoverStyle: {
        paddingTop: 20,
        paddingBottom: 20,
        alignItems: "start"
    },

    // button text menu styles
    userMenuButton: {
        // width: "100%",
        fontSize: "19px",
        fontWeight: "700",
        marginTop: 5,
        '&:hover': {
            backgroundColor: "#E0E0E0"
        }
    },
    activeUserMenuButton: {
        // width: "100%",
        // fontSize: "1.125rem",
        // fontWeight: "700",
        marginTop: 5,
        backgroundColor: "#E0E0E0"
    },
    userMenuButtonText: {
        width : "100%",
        fontSize: "19px",
        fontWeight: "500",
        fontFamily: "roboto",
        letterSpacing: "0.5px"
    },
    // popover button text style
    popoverMenuText: {
        width : "100%",
        fontSize: "0.875rem",
        fontWeight: "400",
        fontFamily: "roboto",
        padding: 5
    },
    popoverMenuButton: {
        
    },
    popoverMenuButtonActive: {

    }
}));

export default function TopHeader(props) {
    const { 
            header, 
            logo, 
            menuButton, 
            toolbar, 
            desktopMenuContainer, 
            drawerContainer, 
            popoverStyle, 
            highlightedMenuButton, 
            userMenuButton, 
            activeUserMenuButton, 
            userMenuButtonText,
            popoverMenuText
        } = useStyles();

    const { currentMenu, dontShowHeader } = props;

    const logoRef = useRef(null);

    const [state, setState] = useState({
        mobileView: false,
        drawerOpen: false,
    });

    const [headerLogoImg, setHeaderLogoImg] = useState(AnuvaadLogo);

    const [showUserPopoverMenuAnchorEle, setShowUserPopoverMenuAnchorEle] = useState(null);
    const [showSettingsPopoverMenuAnchorEle, setShowSettingsPopoverMenuAnchorEle] = useState(null);

    const assignedOrgId = JSON.parse(localStorage.getItem("userProfile"))?.orgID;
    const role = localStorage.getItem("roles");
    const userName = JSON.parse(localStorage.getItem("userProfile"))?.name.trim();

    const { mobileView, drawerOpen } = state;

    useEffect(() => {
        const setResponsiveness = () => {
            return window.innerWidth < 1100
                ? setState((prevState) => ({ ...prevState, mobileView: true }))
                : setState((prevState) => ({ ...prevState, mobileView: false }));
        };

        setResponsiveness();

        window.addEventListener("resize", () => setResponsiveness());

        return () => {
            window.removeEventListener("resize", () => setResponsiveness());
        };
    }, []);

    const displayDesktop = () => {
        return (
            !dontShowHeader && <Toolbar className={toolbar}>
                {femmecubatorLogo()}
                <div>{getMenuButtons()}</div>
                <div>{PopOverMenuButtons()}</div>
            </Toolbar>
        );
    };

    const displayMobile = () => {
        const handleDrawerOpen = () =>
            setState((prevState) => ({ ...prevState, drawerOpen: true }));
        const handleDrawerClose = () =>
            setState((prevState) => ({ ...prevState, drawerOpen: false }));

        return (
            !dontShowHeader && <Toolbar className={toolbar}>
                <div>{femmecubatorLogo()}</div>
                <IconButton
                    {...{
                        edge: "start",
                        color: "#2C2799",
                        "aria-label": "menu",
                        "aria-haspopup": "true",
                        onClick: handleDrawerOpen,
                    }}
                >
                    <MenuIcon />
                </IconButton>

                <Drawer
                    {...{
                        anchor: "right",
                        open: drawerOpen,
                        onClose: handleDrawerClose,
                    }}
                >
                    <div className={drawerContainer}>
                        {/* <div 
                            style={{
                                display : "flex",
                                alignItems: "center",
                                justifyContent: "space-between",
                                marginTop: 5,
                                marginBottom: 5
                            }}
                        > */}
                        {/* {femmecubatorLogo} */}
                        <IconButton
                            {...{
                                edge: "start",
                                color: "#2C2799",
                                "aria-label": "menu",
                                "aria-haspopup": "true",
                                onClick: handleDrawerClose,
                            }}
                        >
                            <CloseIcon />
                        </IconButton>
                        <Divider />
                        {getDrawerChoices(handleDrawerClose)}
                    </div>
                </Drawer>
            </Toolbar>
        );
    };

    const getDrawerChoices = (closeDrawerOnMenuClick) => {
        return (
            <>
                <Typography variant="body2" style={{ marginBottom: 3, marginTop: 3 }}>Main Menu -</Typography>
                {headerMenuConfig.map((el, i) => {
                    return el.menuType === "MAIN" && el.rolesAllowed.includes(role) && assignedOrgId !== "NONMT" &&
                        <div>
                            <Button
                                {...{
                                    key: el.id,
                                    id: el.id,
                                    onClick: () => {
                                        el.onclick(assignedOrgId);
                                        closeDrawerOnMenuClick()
                                    },
                                    style: { textDecoration: "none", color: "#000000", marginTop : 5 },
                                    component: RouterLink,
                                    className: currentMenu === el.id ? highlightedMenuButton : menuButton,
                                }}
                            >
                                {el.title}
                            </Button>
                        </div>

                })}
                <Typography variant="body2" style={{ marginBottom: 3, marginTop: 3 }}>Settings -</Typography>
                {headerMenuConfig.map((el, i) => {
                    return el.menuType === "SETTINGS" && el.rolesAllowed.includes(role) && assignedOrgId !== "NONMT" &&
                        <div>
                            <Button
                                {...{
                                    key: el.id,
                                    id: el.id,
                                    onClick: () => {
                                        el.onclick(assignedOrgId);
                                        closeDrawerOnMenuClick()
                                    },
                                    style: { textDecoration: "none", color: "#000000", marginTop : 5 },
                                    component: RouterLink,
                                    className: currentMenu === el.id ? highlightedMenuButton : menuButton,
                                }}
                            >
                                {el.title}
                            </Button>
                        </div>

                })}
                <Typography variant="body2" style={{ marginBottom: 3, marginTop: 3 }}>Options -</Typography>
                {headerMenuConfig.map((el, i) => {
                    return el.menuType === "USER" && el.rolesAllowed.includes(role) && assignedOrgId !== "NONMT" &&
                        <div>
                            <Button
                                {...{
                                    key: el.id,
                                    id: el.id,
                                    onClick: () => {
                                        el.onclick(assignedOrgId);
                                        closeDrawerOnMenuClick()
                                    },
                                    style: { textDecoration: "none", color: "#000000", marginTop : 5 },
                                    component: RouterLink,
                                    className: currentMenu === el.id ? highlightedMenuButton : menuButton,
                                }}
                            >
                                {el.title}
                            </Button>
                        </div>

                })}
            </>

        );
    };

    const femmecubatorLogo = () => {
        return <img 
                    src={headerLogoImg} 
                    className={logo}
                    ref={logoRef}
                    onError={(({currentTarget})=> {
                        currentTarget.onerror = null;
                        if(!currentTarget.src.includes(AnuvaadLogo)){
                            currentTarget.src = AnuvaadLogo;
                            return
                        }
                    })}
                />
    };

    const getMenuButtons = () => {
        return (
            <Grid container className={desktopMenuContainer}>
                {headerMenuConfig.map((el, i) => {
                    return (
                        el.menuType === "MAIN" && el.rolesAllowed.includes(role) && assignedOrgId !== "NONMT" && <Button
                            {...{
                                key: el.id,
                                id: el.id,
                                onClick: () => { el.onclick(assignedOrgId) },
                                style: { textDecoration: "none", color: "#000000", letterSpacing: "0.5px" },
                                component: RouterLink,
                                className: currentMenu === el.id ? highlightedMenuButton : menuButton,
                            }}
                        >
                            <Typography className={userMenuButtonText}>{el.title}</Typography>
                        </Button>
                    );
                })}
            </Grid>

        )
    };

    const PopOverMenuButtons = () => {
        return (
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Grid container justifyContent="center" alignItems="center" spacing={2}>
                        {(role !== "SUPERADMIN" && role !== "ADMIN") && <Grid item>
                            <div style={{ display: "flex", alignItems: "center" }}>
                                <IconButton
                                    {...{
                                        edge: "start",
                                        color: "#2C2799",
                                        "aria-label": "menu",
                                        "aria-haspopup": "true",
                                    }}
                                    onClick={(e) => setShowSettingsPopoverMenuAnchorEle(e.currentTarget)}
                                >
                                    <SettingsOutlinedIcon fontSize="large" />
                                </IconButton>
                                <Popover
                                    id={"simple-popover"}
                                    open={Boolean(showSettingsPopoverMenuAnchorEle)}
                                    anchorEl={showSettingsPopoverMenuAnchorEle}
                                    onClose={() => setShowSettingsPopoverMenuAnchorEle(null)}
                                    anchorOrigin={{
                                        vertical: 'bottom',
                                        horizontal: 'center',
                                    }}
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'center',
                                    }}
                                    style={{ backgroundColor: "rgba(0,0,0,0)" }}
                                >
                                    <Grid container direction="column" className={popoverStyle}>
                                        {
                                            headerMenuConfig.map((el, i) => {
                                                return (
                                                    el.menuType === "SETTINGS" && el.rolesAllowed.includes(role) && assignedOrgId !== "NONMT" &&
                                                    <Button
                                                        variant="text"
                                                        fullWidth
                                                        className={currentMenu === el.id ? activeUserMenuButton : userMenuButton}
                                                        onClick={() => {
                                                            setShowSettingsPopoverMenuAnchorEle(null)
                                                            el.onclick(assignedOrgId)
                                                        }}
                                                    >
                                                        <Typography className={popoverMenuText} style={{textAlignLast : "left"}}>{el.title}</Typography>
                                                    </Button>
                                                )
                                            })
                                        }
                                    </Grid>
                                </Popover>
                            </div>
                        </Grid>}
                        <Grid item>
                            <div style={{ display: "flex", alignItems: "center" }}>

                                <Button variant="text" color="primary" onClick={(e) => setShowUserPopoverMenuAnchorEle(e.currentTarget)}><IconButton
                                    {...{
                                        edge: "start",
                                        color: "#2C2799",
                                        "aria-label": "menu",
                                        "aria-haspopup": "true",
                                    }}
                                >
                                    <Avatar style={{ backgroundColor: "#2C2799" }}>{userName?.split("")[0].toLocaleUpperCase()}</Avatar>
                                </IconButton>
                                    <Typography variant="subtitle1" style={{fontSize: "1.25rem"}}>{userName?.split(" ")[0]}</Typography>
                                </Button>
                                <Popover
                                    id={"simple-popover"}
                                    open={Boolean(showUserPopoverMenuAnchorEle)}
                                    anchorEl={showUserPopoverMenuAnchorEle}
                                    onClose={() => setShowUserPopoverMenuAnchorEle(null)}
                                    anchorOrigin={{
                                        vertical: 'bottom',
                                        horizontal: 'center',
                                    }}
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'center',
                                    }}
                                    style={{ backgroundColor: "rgba(0,0,0,0)" }}
                                >
                                    <Grid container direction="column" className={popoverStyle}>
                                        <Grid item>
                                            <Typography style={{padding: 10}} variant="caption">Signed in as <b>{role ? role : ""}</b></Typography>
                                        </Grid>
                                        <Divider style={{ marginTop: 5, marginBottom: 5, width: "100%" }} />
                                        {
                                            headerMenuConfig.map((el, i) => {
                                                return (
                                                    el.menuType === "USER" && el.rolesAllowed.includes(role) &&
                                                    <Button
                                                        variant="text"
                                                        fullWidth
                                                        className={currentMenu === el.id ? activeUserMenuButton : userMenuButton}
                                                        onClick={() => {
                                                            setShowUserPopoverMenuAnchorEle(null)
                                                            el.onclick(assignedOrgId)
                                                        }}
                                                    >
                                                        <Typography className={popoverMenuText} style={{textAlignLast : "left"}}>{el.title}</Typography>
                                                    </Button>
                                                )
                                            })
                                        }
                                    </Grid>
                                </Popover>
                            </div>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        )
    }

    return (
        <header>
            <AppBar className={header}>
                {mobileView ? displayMobile() : displayDesktop()}
            </AppBar>
        </header>
    );
}