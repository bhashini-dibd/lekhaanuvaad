import React, { useEffect, useState } from "react";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import OTPInput from "otp-input-react";
import {
  Button,
  IconButton,
  ThemeProvider,
  Typography,
} from "@material-ui/core";
import themeAnuvaad from "../../../theme/web/theme-anuvaad";

const EnterOTPModal = (props) => {
  const [OTP, setOTP] = useState("");
  const {
    open,
    handleClose,
    onResend,
    onSubmit,
    OTPModalTitle,
    hideResendOTPButton,
    showTimer,
    // loading,
  } = { ...props };

  const [time, setTime] = useState(60);
  const [running, setRunning] = useState(true);
  useEffect(() => {
    let interval;
    if (showTimer && running ) {
      interval = setInterval(() => {
        setTime(prevTime => {
          if (prevTime > 0) {
            return prevTime - 1;
          } else if (prevTime === 0) {
            clearInterval(interval);
            setTimeout(() => setTime(60), 60000);
            setRunning(false);
            return prevTime;
          }
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [showTimer,running]);


  console.log(time,"timetimetime",showTimer)
  useEffect(() => {
    setTimeout(function () {
      handleClose();
    }, 600000);
  }, [open]);
  

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
        <DialogTitle id="alert-dialog-title" align="center">
          {OTPModalTitle}
        </DialogTitle>

        <DialogTitle
          style={{ alignSelf: "center", fontSize: "18px", height: "10px" }}
        >
          {" "}
          {!time == 0 && showTimer  && (
            <span>
              Time left: {`${Math.floor(time / 60)}`.padStart(2, 0)}:
              {`${time % 60}`.padStart(2, 0)}
            </span>
          )}
        </DialogTitle>

        <DialogContent
          style={{
            alignSelf: "center",
            margin: !time == 0 ? "15px 50px 50px 50px" : "15px 50px 50px 50px",
            display: "flex",
          }}
        >
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
            color="primary"
            variant="outlined"
            style={{ borderRadius: 15 }}
          >
            Cancel
          </Button>
          {!hideResendOTPButton && (
            <Button
              onClick={() => {
                onResend();
                setOTP("");
                setTime(60);
                setRunning(true)
              }}
              color="primary"
              variant="contained"
              style={{ borderRadius: 15 }}
              disabled={!time == 0 && showTimer}
            >
              Resend OTP

            </Button>
          )}

          <Button
            onClick={() => onSubmit(OTP)}
            color="primary"
            variant="contained"
            disabled={!OTP}
            style={{ borderRadius: 15 }}
          >
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </ThemeProvider>
  );
};

export default EnterOTPModal;
