import wx
import math
import time
import BackEnd
import AutoTurn

class GamePanel(wx.Panel):
    dragStartX = 0
    dragStartY = 0
    rootX = 0
    rootY = 0
    game = BackEnd.UTicTacToe()
    dimensionChanged = True;
    rootChanged = True;
    dragging = False;
    
    """ class GamePanel creates a panel to draw on, inherits wx.Panel """
    def __init__(self, parent, id):
        # create a panel
        wx.Panel.__init__(self, parent, id)
        # double buffering allows smoother redraws without flickering
        self.SetDoubleBuffered(True)
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnDrag)
        self.Bind(wx.EVT_LEFT_UP, self.OnUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_TIMER, self.TimedRefresh)

        self.timer = wx.Timer(self)

    #TODO AI player

    def Draw(self):
        self.dc.SetLogicalOrigin(self.rootX, self.rootY)

        xStartCoord = self.game.minX * 50
        yStartCoord = self.game.minY * 50
        xEndCoord = (self.game.maxX + 1) * 50
        yEndCoord = (self.game.maxY + 1) * 50
                            
        for x in range(self.game.minX, self.game.maxX + 2):
            self.dc.DrawLine(x * 50, yStartCoord, x * 50, yEndCoord)
            #print("Drawing line ", x * 50, ", ", yStartCoord, " to ", x * 50, ", ", yEndCoord)
        for y in range(self.game.minY, self.game.maxY + 2):
            self.dc.DrawLine(xStartCoord, y * 50, xEndCoord, y * 50)
            #print("Drawing line ", xStartCoord, ", ", y * 50, " to ", xEndCoord, ", ", y * 50)

        for coords in self.game.currentBoard.keys():
            x = int(coords[0] * 50)
            y = int(coords[1] * 50)
                                
            if (self.game.currentBoard[coords] == 0):
                self.dc.DrawCircle(x + 25, y + 25, 25)
            elif (self.game.currentBoard[coords] == 1):
                self.dc.DrawLine(x, y, x + 50, y + 50)
                self.dc.DrawLine(x + 50, y, x, y + 50)

        for coord in self.game.structuresForCoords:
            structText = str(coord[0]) + ", " + str(coord[1])
            
            #for struct in self.game.structuresForCoords[coord]:
                #for coord in struct.getTipCoords():
                 #   self.dc.DrawText(str(struct.id) + ", ", coord[0] * 50, coord[1] * 50)
                #structText += str(struct.id) + ", "

            self.dc.DrawText(structText, coord[0] * 50, coord[1] * 50)
            

        for victoryStruct in self.game.detectVictory():
            self.dc.SetPen(wx.Pen("red"))
            self.dc.SetBrush(wx.Brush("red", wx.BRUSHSTYLE_TRANSPARENT))
            for coord in victoryStruct.coords:
                gX = coord[0] * 50;
                gY = coord[1] * 50;
                self.dc.DrawRectangle(gX + 1, gY + 1, 49, 49)
            

    def TimedRefresh(self, event):
        self.Refresh()

    def OnPaint(self, evt):
        """set up the device context (DC) for painting"""
        self.dc = wx.PaintDC(self)
        self.dc.SetPen(wx.Pen("black"))
        self.dc.SetBrush(wx.Brush("grey", wx.SOLID))
        # set x, y, w, h for rectangle
        self.Draw()
        del self.dc
        # "60 frames per second"
        self.timer.Start(16)

    def OnDown(self, event):
        x, y = event.GetPosition()
        #print("Click coordinates: X=",x," Y=",y)
        self.dragStartX = x
        self.dragStartY = y

    def OnRightUp(self, event):
        x, y = event.GetPosition()
        xCoord = math.floor((x + self.rootX) / 50)
        yCoord = math.floor((y + self.rootY) / 50)

        autoTurn = AutoTurn.AutoTurn()
        autoTurn.makeMove(self.game)
        self.Refresh()

    def OnUp(self, event):
        myCursor= wx.Cursor(wx.CURSOR_DEFAULT)
        self.SetCursor(myCursor)
        x, y = event.GetPosition()

        #print("Click Up coordinates: X=",x," Y=",y)
        
        #print (self.dragging)
        if (self.dragging == True):            
            deltaX = self.dragStartX - x
            deltaY = self.dragStartY - y
            #print("Delta: ", deltaX, deltaY)
            self.rootX += deltaX;
            self.rootY += deltaY;
            self.dragging = False
            return

        # adjust clicked coordinates to account for dragging
        xCoord = math.floor((x + self.rootX) / 50)
        yCoord = math.floor((y + self.rootY) / 50)
        self.game.playSpace((xCoord, yCoord))
        self.Refresh()

    def OnDrag(self, event):
        x, y = event.GetPosition()
        if not event.Dragging():
            event.Skip()
            return
        event.Skip()
        # make it clear to the user they're dragging things around
        myCursor= wx.Cursor(wx.CURSOR_HAND)
        self.SetCursor(myCursor)
        #print("Dragging position", x, y)
        #self.rootX -= x - self.dragStartX;
        #self.rootY -= y - self.dragStartY
        self.dragging = True
        #print("Root", self.rootX, ' ', self.rootY)

app = wx.App()
# create a window/frame, no parent, -1 is default ID
frame = wx.Frame(None, -1, "Unlimited Tic Tac Toe", size = (500, 500))
# call the derived class, -1 is default ID
GamePanel(frame,-1)
# show the frame
frame.Show(True)
# start the event loop
app.MainLoop()
