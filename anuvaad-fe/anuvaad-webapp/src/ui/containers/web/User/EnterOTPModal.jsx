import React, { useEffect, useState } from "react";
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import OTPInput from "otp-input-react";
import { Button, IconButton, ThemeProvider, Typography } from "@material-ui/core";
import themeAnuvaad from "../../../theme/web/theme-anuvaad";

const EnterOTPModal = (props) => {
    const [OTP, setOTP] = useState("");

    const {
        open,
        handleClose,
        onResend,
        onSubmit,
        OTPModalTitle,
        hideResendOTPButton
    } = { ...props };

    return (
        <ThemeProvider theme={themeAnuvaad}>
            <Dialog
                open={open}
                // onClose={handleClose}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
                fullWidth
                style={{ backgroundColor: "rgba(255,255,255,0.6)" }}
            >
                <DialogTitle id="alert-dialog-title">{OTPModalTitle}</DialogTitle>
                <DialogContent style={{ alignSelf: "center", margin: 50, display: "flex" }}>
                    <OTPInput
                        value={OTP}
                        onChange={setOTP}
                        autoFocus
                        OTPLength={6}
                        otpType="number"
                    />
                </DialogContent>
                <DialogActions>
                    <Button
                        onClick={() => {
                            handleClose();
                            setOTP("");
                        }}
                        color="primary" variant="outlined" style={{ marginRight: "auto", borderRadius: 15 }}>
                        Cancel
                    </Button>
                    {!hideResendOTPButton && <Button onClick={()=>{
                        onResend();
                        setOTP("");
                    }} color="primary" variant="contained" style={{ borderRadius: 15 }}>
                        Resend OTP
                    </Button>}
                    <Button onClick={() => onSubmit(OTP)} color="primary" variant="contained" disabled={!OTP} style={{ borderRadius: 15 }}>
                        Submit
                    </Button>
                </DialogActions>
            </Dialog>
        </ThemeProvider>

    )
}

export default EnterOTPModal