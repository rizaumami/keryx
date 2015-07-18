import os.path
import urllib
import wx
import hashlib
import wx.lib.delayedresult as delayedresult

import lib
from lib import consts, log

class download(wx.Frame):
    """This demos simplistic use of delayedresult module."""
    def __init__(self, parent, endfunc, files, extract=False, overwrite=False):
        wx.Frame.__init__(self, None, title=_("Downloading..."))
        self.parent = parent
        self.files = files
        self.function = endfunc
        self.extract = extract
        self.overwrite = overwrite
        self.retries = 1

        #TODO: Add overwrite function

        self.SetIcon(wx.Icon(consts.fileIco, wx.BITMAP_TYPE_ICO))
        panel = wx.Panel(self)
        loading = wx.StaticText(panel, -1, _("This may take a while. Please be patient."))
        self.gauge = wx.Gauge(panel)
        #cancelBtn  = wx.Button(panel, -1, "Cancel")

        self.cur = wx.StaticText(panel, -1, _("Current Transfer:"))
        self.cur.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.current = wx.StaticText(panel, -1, "\n")
        self.download_gauge = wx.Gauge(panel)
        self.status = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)

        status = wx.BoxSizer()
        status.Add(self.cur, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        status.Add(self.current, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(loading, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        main.Add(self.gauge, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(status)
        main.Add(self.download_gauge, 0, wx.EXPAND|wx.ALL, 5)
        main.Add(self.status, 1, wx.EXPAND|wx.ALL, 5)
        #main.Add(cancelBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)

        panel.SetSizer(main)
        self.Center()
        self.Show()

        self.jobID = 0
        self.abortEvent = delayedresult.AbortEvent()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #self.Bind(wx.EVT_BUTTON, self.handleAbort, cancelBtn)
        self.Bind(wx.EVT_TIMER, self.TimerHandler)

        self.timer = wx.Timer(self)
        self.timer.Start(100)

        self.parent.Enable(False)
        self.handleGet(None)

    def TimerHandler(self, event): self.gauge.Pulse()

    def OnClose(self, event):
        """Only needed because in demo, closing the window does not kill the
        app, so worker thread continues and sends result to dead frame; normally
        your app would exit so this would not happen."""
        #if self.buttonAbort.IsEnabled():
            #self.log( "Exiting: Aborting job %s" % self.jobID )
            #self.handleAbort(None)
        self.Show()

    def handleGet(self, event):
        """Compute result in separate thread, doesn't affect GUI response."""
        #self.buttonGet.Enable(False)
        #self.buttonAbort.Enable(True)
        self.abortEvent.clear()
        self.jobID += 1

        log.info( "Starting job %s in producer thread: GUI remains responsive"
                  % self.jobID )
        delayedresult.startWorker(self._resultConsumer, self._resultProducer,
                                  wargs=(self.jobID,self.abortEvent), jobID=self.jobID)


    def _resultProducer(self, jobID, abortEvent):
        """Downloads the files in self.files"""
        self.numfiles = len(self.files)
        msg = _("Downloading ") + str(self.numfiles) + " " + _("file(s)") + "\n"
        wx.CallAfter(self.LogMessage, msg)

        if consts.proxy_enabled:
            if consts.http_proxy['http'][0:7] != 'http://':
                proxy = {'http://':consts.http_proxy['http']}
            else:
                proxy = consts.http_proxy
            downloader = Downloader(proxy)
        else:
            downloader = Downloader()

        failed = self.files[:]
        self.numfile = 0
        for data in self.files:
            if abortEvent(): return [1, failed]
            url = data[0]
            filepath = data[1]
            end = url.split('/')
            protocol = end[0] + '//'
            site = end[2]
            end = end[len(end) - 1]
            if len(data) <= 2:
                checksum = {}
            else:
                checksum = data[2]

            msg = _("Starting") + " " + end
            wx.CallAfter(self.SetFile, msg)
            #TODO: Change this to file progress (move to self.progress)

            self.curfile = end
            self.numfile += 1
            if os.path.exists(filepath):
                if not self.overwrite:
                    if self._verify(filepath, checksum) >= 1:
                        msg = _("Skipped: ") + end + "\n" + _("Reason: ") + _("File already exists.") + "\n"
                        wx.CallAfter(self.LogMessage, msg)
                        failed.remove(data)
                        continue
                    else:
                        msg = _("Deleted: ") + filepath + "\n" + _("Reason: ") + _("Existing file failed checksum verify.") + "\n"
                        wx.CallAfter(self.LogMessage, msg)
                os.remove(filepath)
            retries = 0
            success = False
            while retries <= self.retries:

                try: # Attempt to download the file
                    msg = _("Downloading: ") + url + "\n"
                    if retries != 0: msg = _("Retrying: ")+"[%i/%i] " % (retries, self.retries) + url + "\n"
                    wx.CallAfter(self.LogMessage, msg)

                    downloader.retrieve(url, filepath, self.progress)
                    
                    if self._verify(filepath, checksum) == 0:
                        msg = _("Failed verify: ") + filepath + "\n"
                        wx.CallAfter(self.LogMessage, msg)
                        os.remove(filepath)
                        retries += 1
                        continue

                    success = True
                    failed.remove(data)
                    msg = _("Success: ") + filepath + "\n"
                    wx.CallAfter(self.LogMessage, msg)

                    if self.extract:
                        msg = _("Extracting") + " " + end
                        wx.CallAfter(self.SetFile, msg)
                        try:
                            import gzip
                            infile = gzip.open(filepath, 'rb')
                            outfile = open(filepath[:-3], 'wb')
                            outfile.write(infile.read())
                            outfile.close()
                            infile.close()
                            os.remove(filepath)
                        except:  # Failed to extract
                            msg = _("Unable to extract: ") + filepath
                            wx.CallAfter(self.LogMessage, msg)
                    break

                except IOError, e: # Failed downloading
                    msg = _("Failed: ") + url + "\n" + _("Reason: ") + str(e) + "\n"
                    wx.CallAfter(self.LogMessage, msg)
                    retries += 1


        msg = _("Downloaded: ") + str(len(self.files) - len(failed)) + ", " + _("Failed: ") + str(len(failed)) + "\n"
        wx.CallAfter(self.LogMessage, msg)
        if failed == []:
            wx.CallAfter(self.DisplayMessage,_("All downloads have been completed successfully."), _("Download Complete"))
            result = [0,failed]
        else:
            wx.CallAfter(self.DisplayMessage, _("Some downloads failed to complete.") + "\n" +_("Please check") + " " + os.path.join(consts.dirLog, "log") + " " + _("for more details."), _("Download Failed"))
            result = [1,failed]
        return result

    def _verify(self, filename, checksum, cspriority=['SHA256','SHA1','MD5sum']):
        """ Does a hash check on 'filename' as per hashes in 'checksum' dict. Currently only supports sha256, sha1, md5."""
        if cspriority != []:
            checks = [x for x in cspriority if checksum.has_key(x)]
            if checks == []: return 2
        else:
            checks = checksum.keys()
        if checks == []: return 2

        if checks[0] == 'SHA256':
            check = hashlib.sha256()
        elif checks[0] == 'SHA1':
            check = hashlib.sha1()
        elif checks[0] == 'MD5sum':
            check = hashlib.md5()
        else:
            return 2
        
        try:
            fd = open(filename, 'rb')
            data = fd.read(1024*64)
            while data:
                check.update(data)
                data=fd.read(1024*64)
            fd.close()
            if check.hexdigest() == checksum[checks[0]]:
                return 1
            return 0
        except:
            return 2

    def progress(self, blocks, size, total):
        if blocks*size > total: fraction = float(total)/float(total)
        else:                   fraction = float(blocks*size)/float(total)

        wx.CallAfter(self.SetGauge, int(round(fraction*100,2)))
        msg = self.curfile + "\n" + str(int(round(fraction*100,2))) + " % of " + lib.convert_file_size(total) + " - File "+ str(self.numfile) + "/" + str(self.numfiles)
        wx.CallAfter(self.SetFile, msg)

    def LogMessage(self, msg):
        log.info(msg[:-1])
        self.status.AppendText(msg)
    def DisplayMessage(self, msg, caption): 
        wx.MessageBox(msg, caption)
    def SetGauge(self, val): 
        self.download_gauge.SetValue(val)
    def SetFile(self, val): 
        self.current.SetLabel(val)

    def handleAbort(self, event):
        """Abort the result computation."""
        log.info( "Aborting result for job %s" % self.jobID )
        #self.buttonGet.Enable(True)
        #self.buttonAbort.Enable(False)
        self.abortEvent.set()


    def _resultConsumer(self, delayedResult):
        jobID = delayedResult.getJobID()
        assert jobID == self.jobID
        try:
            result = delayedResult.get()
        except Exception, exc:
            log.info( "Result for job %s raised exception: %s" % (jobID, exc) )
            return

        # output result
        #log.info( "Got result for job %s: %s" % (jobID, result) )
        self.parent.Enable()
        self.Destroy()
        if self.function: self.function()

class Downloader(urllib.FancyURLopener):
    def __init__(self, proxy={}):
        urllib.FancyURLopener.__init__(self, proxy)

    def prompt_user_passwd(self, host='', realm=''):
        return (consts.proxy_username, consts.proxy_password)

