@namespace
class Tobbie:
    ADL_R: number = 0
    ADH_R: number = 0
    ADL_L: number = 0
    ADH_L: number = 0
    Read_LIR: number = 0
    Read_RIR: number = 0
    event_src_ir = 12
    event_ir_sensor = 1
    Motor_R: bool = False
    Motor_L: bool = False
    PX: number = 0
    PY: number = 0
    Force: number = 10
    def IR_sensorL(irdataL: number):
        # 此為中斷觸發方塊
        
        def on_in_background():
            flag = False
            last_flag = False
            while True:
                ob: bool = LBlock()
                if ob:
                    flag = True
                else:
                    flag = False
                if flag != last_flag:
                    # 300ms
                    if flag:
                        control.raise_event(event_src_ir, event_ir_sensor)
                        basic.pause(300)
                    last_flag = flag
                basic.pause(1)
        control.in_background(on_in_background)
        
    # 
    # 背景執行紅外線測距
    # @param irdata_Set ; eg: 512
    # 
    # //% blockId="IR_EVENTL" block="ON obstacles on the left: |%irdata_Set"
    # //% irdata_Set.min=0 irdata_Set.max=1023
    # //% blockGap=10 weight=99   //代表其重要性，越重放越高
    # export function onIRL(irdata_Set: number = 512, handler: Action) {
    # IR_sensorL(irdata_Set);
    # control.onEvent(event_src_ir, event_ir_sensor, handler); 
    # }
    # function IR_sensorR(irdata: number) { 
    # control.inBackground(() => {
    # let flag = false
    # let last_flag = false
    # while (true) {
    # let ob: boolean = LBlock();
    # if(ob){flag=true}else{flag=false}
    # if (flag != last_flag) {
    # if (flag) { 
    # control.raiseEvent(event_src_ir, event_ir_sensor)
    # basic.pause(3)
    # }
    # last_flag = flag
    # }
    # basic.pause(1)
    # }   
    # }      
    # )
    # }
    """
    Read the value sensed by the right side of the infrared sensor.
    
    """
    # % blockId="Read_RBolck" block="get right IR data(return 0~1024)"
    # % blockGap=5 weight=65                 //與下一個方塊的間隙及排重
    def Read_RBlock():
        global ADL_R, ADH_R, Read_RIR
        basic.pause(100)
        ADL_R = pins.analog_read_pin(AnalogPin.P2)
        pins.digital_write_pin(DigitalPin.P12, 1)
        control.wait_micros(250)
        ADH_R = pins.analog_read_pin(AnalogPin.P2)
        pins.digital_write_pin(DigitalPin.P12, 0)
        if pins.digital_read_pin(DigitalPin.P8) == 1:
            Read_RIR = ADH_R - ADL_R
        return (Read_RIR)
    """
    Read the value sensed by the left side of the infrared sensor.
    
    """
    # % blockId="Read_LBolck" block="get left IR data(trtuen 0~1024)"
    # % blockGap=15 weight=60                 //與下一個方塊的間隙及排重
    def Read_LBlock():
        global ADL_L, ADH_L, Read_LIR
        basic.pause(100)
        ADL_L = pins.analog_read_pin(AnalogPin.P1)
        pins.digital_write_pin(DigitalPin.P12, 1)
        control.wait_micros(250)
        ADH_L = pins.analog_read_pin(AnalogPin.P1)
        pins.digital_write_pin(DigitalPin.P12, 0)
        Read_LIR = ADH_L - ADL_L
        return (Read_LIR)
    """
    
    Determine if there are obstacles on the right side.
    @param thresholdR ; eg: 512
    
    """
    # % blockId="RBolck" block="is the right IR over %thresholdR strength"
    # % thresholdR.min=0 thresholdR.max=1023
    # % blockGap=5 weight=58
    def RBlock(thresholdR: number = 512):
        global ADL_R, ADH_R
        basic.pause(100)
        ADL_R = pins.analog_read_pin(AnalogPin.P2)
        pins.digital_write_pin(DigitalPin.P12, 1)
        control.wait_micros(250)
        ADH_R = pins.analog_read_pin(AnalogPin.P2)
        pins.digital_write_pin(DigitalPin.P12, 0)
        if ((ADH_R - ADL_R) > thresholdR) and (pins.digital_read_pin(DigitalPin.P8) == 1):
            # basic.showIcon(IconNames.House)
            return (True)
        else:
            # basic.showIcon(IconNames.Cow)
            return (False)
    """
    
    Determine if there are obstacles on the left side.
    @param thresholdL ; eg: 512
    
    """
    # % blockId="LBolck" block="is the left IR over %thresholdL strength"
    # % thresholdL.min=0 thresholdL.max=1023
    # % blockGap=10 weight=57
    def LBlock(thresholdL: number = 512):
        global ADL_L, ADH_L
        basic.pause(100)
        ADL_L = pins.analog_read_pin(AnalogPin.P1)
        pins.digital_write_pin(DigitalPin.P12, 1)
        control.wait_micros(250)
        ADH_L = 0
        if pins.digital_read_pin(DigitalPin.P8) == 1:
            ADH_L = pins.analog_read_pin(AnalogPin.P1)
            pins.digital_write_pin(DigitalPin.P12, 0)
        if (ADH_L - ADL_L) > thresholdL:
            # 512) { 
            # basic.showIcon(IconNames.House)
            return (True)
        else:
            # basic.showIcon(IconNames.Cow)
            return (False)
    # 輸出脈波
    # % blockId="IRbolck" block="Out pulse & show-04"
    # % blockGap=10 weight=55
    # export function IRblock() {
    # ADL_L = pins.analogReadPin(AnalogPin.P1)
    # ADL_R = pins.analogReadPin(AnalogPin.P2)
    # pins.digitalWritePin(DigitalPin.P12, 1)
    # control.waitMicros(250)
    # ADH_L = pins.analogReadPin(AnalogPin.P1)
    # ADH_R = pins.analogReadPin(AnalogPin.P2)
    # pins.digitalWritePin(DigitalPin.P12, 0)
    # if ((ADH_L-ADL_L) > 512) { 
    # basic.showIcon(IconNames.House)
    # led.plot(0, 0)
    # led.unplot(0,4)
    # } else {
    # basic.showIcon(IconNames.Cow)
    # led.plot(0, 4)
    # led.unplot(0,0)
    # }
    # if ((ADH_R-ADL_R) > 512) { 
    # basic.showIcon(IconNames.House)
    # led.plot(4, 0)
    # led.unplot(4, 4)
    # } else {
    # basic.showIcon(IconNames.Cow)
    # led.plot(4, 4)
    # led.unplot(4,0)
    # }
    # return(true)       
    # }
    """
    
    Tobbie-II walks forward.
    
    """
    # % blockId="forward" block="Tobbie-II walking forward"
    # % blockGap=3 weight=35
    def forward():
        if pins.digital_read_pin(DigitalPin.P8) == 1:
            pins.digital_write_pin(DigitalPin.P13, 1)
            pins.digital_write_pin(DigitalPin.P14, 0)
    """
    
    Tobbie-II walks backward.
    
    """
    # % blockId="backward" block="Tobbie-II walking backward"
    # % blockGap=3  weight=34
    def backward():
        global Force
        if Force != 0:
            pins.digital_write_pin(DigitalPin.P13, 0)
            pins.digital_write_pin(DigitalPin.P14, 1)
            Force = Force - 1
        if pins.digital_read_pin(DigitalPin.P8) == 1:
            Force = 10
    """
    
    Tobbie-II stops walking.
    
    """
    # % blockId="stopwalk" block="Tobbie-II stop walking"
    # % blockGap=10 weight=33
    def stopwalk():
        pins.digital_write_pin(DigitalPin.P13, 0)
        pins.digital_write_pin(DigitalPin.P14, 0)
    """
    
    Tobbie-II rotates to the right.
    
    """
    # % blockId="rightward" block="Tobbie-II turns right"
    # % blockGap=3  weight=32
    def rightward():
        global Motor_L, Motor_R
        pins.digital_write_pin(DigitalPin.P15, 0)
        pins.digital_write_pin(DigitalPin.P16, 1)
        Motor_L = False
        Motor_R = True
    """
    
    Tobbie-II rotates to the left.
    
    """
    # % blockId="leftward" block="Tobbie-II turns left"
    # % blockGap=3  weight=31
    def leftward():
        global Motor_L, Motor_R
        pins.digital_write_pin(DigitalPin.P15, 1)
        pins.digital_write_pin(DigitalPin.P16, 0)
        Motor_L = True
        Motor_R = False
    """
    
    Tobbie-II stops rotating.
    
    """
    # % blockId="stopturn" block="Tobbie-II stops rotating."
    # % blockGap=10 weight=30
    def stopturn():
        global Motor_L, Motor_R
        if Motor_L or Motor_R:
            if Motor_R:
                pins.digital_write_pin(DigitalPin.P15, 1)
                pins.digital_write_pin(DigitalPin.P16, 0)
            else:
                pins.digital_write_pin(DigitalPin.P15, 0)
                pins.digital_write_pin(DigitalPin.P16, 1)
            basic.pause(50)
        if pins.digital_read_pin(DigitalPin.P8) == 1:
            pins.digital_write_pin(DigitalPin.P15, 0)
            pins.digital_write_pin(DigitalPin.P16, 0)
            Motor_L = False
            Motor_R = False
    """
    
    Tobbie-II stamps his foot for a certain number of times.
    @param time describe parameter here, eg:5
    
    """
    # % blockId="vibrate" block="Tobbie-II stamps %time times"
    # % time.min=1 time.max=100
    # % blockGap=5 weight=25
    # % advanced=true
    def vibrate(time: number):
        for i in range(time):
            pins.digital_write_pin(DigitalPin.P13, 1)
            # 向前
            pins.digital_write_pin(DigitalPin.P14, 0)
            basic.pause(150)
            pins.digital_write_pin(DigitalPin.P13, 0)
            # 向後
            pins.digital_write_pin(DigitalPin.P14, 1)
            basic.pause(150)
        pins.digital_write_pin(DigitalPin.P13, 0)
        # 停止
        pins.digital_write_pin(DigitalPin.P14, 0)
    """
    
    Tobbie-II shakes his head for a certain number of times.
    @param time describe parameter here, eg:5
    
    """
    # % blockId="shake_head" block="Tobbie-II shakes head %time times"
    # % time.min=1 time.max=100
    # % blockGap=5 weight=26
    # % advanced=true
    def shake_head(time2: number):
        for j in range(time2):
            pins.digital_write_pin(DigitalPin.P15, 1)
            # 左轉
            pins.digital_write_pin(DigitalPin.P16, 0)
            basic.pause(250)
            pins.digital_write_pin(DigitalPin.P15, 0)
            # 右轉
            pins.digital_write_pin(DigitalPin.P16, 1)
            basic.pause(250)
        pins.digital_write_pin(DigitalPin.P15, 0)
        # 停止行走
        pins.digital_write_pin(DigitalPin.P16, 0)
    """
    
    Tobbie-II repeats the dance for for a certain number of times.
    @param time describe parameter here, eg:5
    
    """
    # % blockId="dance" block="Tobbie-II dances %time times"
    # % time.min=1 time.max=100
    # % blockGap=5 weight=24
    # % advanced=true
    def dance(time3: number):
        for k in range(time3):
            pins.digital_write_pin(DigitalPin.P13, 0)
            # 向後
            pins.digital_write_pin(DigitalPin.P14, 1)
            pins.digital_write_pin(DigitalPin.P15, 0)
            # 右轉
            pins.digital_write_pin(DigitalPin.P16, 1)
            basic.pause(250)
            pins.digital_write_pin(DigitalPin.P13, 1)
            # 向前
            pins.digital_write_pin(DigitalPin.P14, 0)
            pins.digital_write_pin(DigitalPin.P15, 1)
            # 左轉
            pins.digital_write_pin(DigitalPin.P16, 0)
            basic.pause(250)
        pins.digital_write_pin(DigitalPin.P13, 0)
        pins.digital_write_pin(DigitalPin.P14, 0)
        pins.digital_write_pin(DigitalPin.P15, 0)
        pins.digital_write_pin(DigitalPin.P16, 0)
    """
    
    Tobbie II shows his mood on the face (APP only).
    @param RX_Data describe parameter here
    
    """
    # % blockId="BLE_DOT" block="Tobbie II shows mood on face(APP only) %RX_Data"
    # % blockGap=5 weight=23
    # % advanced=true
    def drawface(RX_Data: str):
        basic.clear_screen()
        for PY2 in range(5):
            PLOT_DATA: number = int(RX_Data.substr(PY2 * 2 + 1, 2))
            for PX2 in range(5):
                if PLOT_DATA % 2 == 1:
                    led.plot(PX2, PY2)
                    PLOT_DATA = PLOT_DATA - 1
                PLOT_DATA = PLOT_DATA / 2
        # Tutaj funkcja Bluetooth MUSI BYĆ OSOBNO
        
        def on_bluetooth_connected():
            basic.show_icon(IconNames.YES)
            # Możesz tutaj użyć funkcji z `Tobbie`, np.:
            Tobbie.drawface("FF00FF")
        bluetooth.on_bluetooth_connected(on_bluetooth_connected)
        