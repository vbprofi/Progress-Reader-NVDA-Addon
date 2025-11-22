# progressReader.py
# NVDA Addon: ProgressReader
# A global plugin for NVDA that announces the progress of the progress bar on pressing a button.
# Author: Imam Kahraman
# Contact: imam.kahraman@googlemail.com
# GitHub: https://github.com/vbprofi/Progress-Reader-NVDA-Addon/
# Version: 0.3.0
# License: GNU General Public License v3 (GPL-3.0)
# License File: https://www.gnu.org/licenses/gpl-3.0.txt
# Copyright (C) 2024-2025 Imam Kahraman
# Released under GNU General Public License v3 (GPL-3.0)
# License File: https://www.gnu.org/licenses/gpl-3.0.txt

import globalPluginHandler
import ui
import api
from scriptHandler import script
import addonHandler
import controlTypes
import UIAHandler
from NVDAObjects import NVDAObject
from queue import Queue
import re
import wx
from gui.settingsDialogs import SettingsPanel, NVDASettingsDialog
from gui import guiHelper
import gui
import config
import webbrowser
from globalCommands import SCRCAT_CONFIG

addonHandler.initTranslation()

# configuration
ADDON_CONF_SECTION = "progressReader"
DEFAULT_INTERVAL_MS = 2000  # intern in Millisekunden

def _getConfigInterval():
	try:
		return int(config.conf.get(ADDON_CONF_SECTION, {}).get("refreshInterval", DEFAULT_INTERVAL_MS))
	except Exception:
		return DEFAULT_INTERVAL_MS

def _setConfigInterval(value):
	d = config.conf.get(ADDON_CONF_SECTION, {})
	d["refreshInterval"] = int(value)
	config.conf[ADDON_CONF_SECTION] = d
	try:
		config.conf.save()
	except Exception:
		pass

# Settings Panel
class ProgressReaderSettingsPanel(SettingsPanel):
	"""Settings panel for Progress Reader"""
	title = _("Progress Reader")
	id = "progressReader"

	def makeSettings(self, settingsSizer):
		# Use sizer as NVDA passes it on
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		currentIntervalMs = _getConfigInterval()
		# Display in seconds for the user (integer)
		currentIntervalSeconds = int(round(currentIntervalMs / 1000.0))

		# Label: Seconds
		lbl = wx.StaticText(self, label=_("Aktualisierungsintervall (Sekunden):"))
		sHelper.addItem(lbl)

		# Create SpinCtrl, set range and value (seconds)
		self.intervalCtrl = wx.SpinCtrl(self, style=wx.SP_ARROW_KEYS)
		# 1s .. 300s (5 minutes) as a reasonable range
		self.intervalCtrl.SetRange(1, 300)
		self.intervalCtrl.SetValue(str(currentIntervalSeconds))
		sHelper.addItem(self.intervalCtrl)

		# reset button
		btnRow = guiHelper.BoxSizerHelper(self, orientation=wx.HORIZONTAL)
		self.resetBtn = wx.Button(self, label=_("Zurücksetzen"))
		btnRow.addItem(self.resetBtn)
		# donation-Button
		self.donateBtn = wx.Button(self, label=_("Spenden"))
		btnRow.addItem(self.donateBtn)
		sHelper.addItem(btnRow.sizer)

		# Bind-Handler
		def _onReset(evt):
			defaultSeconds = int(round(DEFAULT_INTERVAL_MS / 1000.0))
			self.intervalCtrl.SetValue(str(defaultSeconds))
			ui.message(_("Intervall auf Standard zurückgesetzt: {} s").format(defaultSeconds))
		self.resetBtn.Bind(wx.EVT_BUTTON, _onReset)

		def _onDonate(evt):
			PAYPAL_DONATE_URL = "https://www.paypal.com/donate/?hosted_button_id=DB9N3QDZLR822"
			try:
				webbrowser.open(PAYPAL_DONATE_URL)
				ui.message(_("Spenden-Seite im Browser geöffnet"))
			except Exception:
				ui.message(_("Konnte die Spenden-Seite nicht öffnen"))
		self.donateBtn.Bind(wx.EVT_BUTTON, _onDonate)

	def postInit(self):
		# Focus on control, if possible
		try:
			self.intervalCtrl.SetFocus()
		except Exception:
			pass

	def onSave(self):
		try:
			newSeconds = int(self.intervalCtrl.GetValue())
			newMs = newSeconds * 1000
			GlobalPlugin.refreshInterval = newMs
			_setConfigInterval(newMs)
			ui.message(_("Intervall gespeichert: {} ms").format(newMs))
			inst = GlobalPlugin.getInstanceIfAny()
			if inst and inst.refreshFrame:
				inst._startAutoRefresh()
		except Exception:
			ui.message(_("Ungültiger Intervallwert"))

	def onDiscard(self):
		# nothing else is needed
		pass


# Panel registration during import (more robust for NVDA 2025+)
try:
	# Try the new API first
	from gui import settings as guiSettings
	if hasattr(guiSettings, "registerSettingsPanel"):
		try:
			guiSettings.registerSettingsPanel(ProgressReaderSettingsPanel)
		except Exception:
			# fallback to older mechanism below
			if ProgressReaderSettingsPanel not in NVDASettingsDialog.categoryClasses:
				NVDASettingsDialog.categoryClasses.append(ProgressReaderSettingsPanel)
	else:
		# Fallback: classic mechanism
		if ProgressReaderSettingsPanel not in NVDASettingsDialog.categoryClasses:
			NVDASettingsDialog.categoryClasses.append(ProgressReaderSettingsPanel)
except Exception:
	# final fallback
	try:
		if ProgressReaderSettingsPanel not in NVDASettingsDialog.categoryClasses:
			NVDASettingsDialog.categoryClasses.append(ProgressReaderSettingsPanel)
	except Exception:
		pass


def disableInSecureMode(decoratedCls):
	try:
		import globalVars
		if getattr(globalVars, "appArgs", None) and getattr(globalVars.appArgs, "secure", False):
			return globalPluginHandler.GlobalPlugin
	except Exception:
		pass
	return decoratedCls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""NVDA GlobalPlugin: Window with auto-refresh for progress bars."""

	refreshInterval = _getConfigInterval()
	_instance = None

	@classmethod
	def getInstanceIfAny(cls):
		return cls._instance

	def __init__(self):
		super().__init__()
		GlobalPlugin._instance = self

		self.category = _("Progress Reader")
		self.refreshFrame = None
		self.refreshText = None  # wx.TextCtrl
		self.refreshTimer = None

		# Watch list for found progress bar windows/objects
		# List of NVDA objects found during remembered
		self.rememberedProgressObjects = []
		self.rememberingActive = False

		# Load configuration at startup
		GlobalPlugin.refreshInterval = _getConfigInterval()

	def terminate(self):
		# Remove panel registration cleanly when add-on is unloaded
		try:
			if ProgressReaderSettingsPanel in NVDASettingsDialog.categoryClasses:
				NVDASettingsDialog.categoryClasses.remove(ProgressReaderSettingsPanel)
		except Exception:
			pass
		# stop timer and destroy frame if needed
		self._stopAutoRefresh()
		if self.refreshFrame:
			try:
				self.refreshFrame.Destroy()
			except Exception:
				pass
			self.refreshFrame = None
		GlobalPlugin._instance = None

	def onSettings(self, evt):
		# Opens the NVDA Settings dialog directly with our panel
		gui.mainFrame.popupSettingsDialog(NVDASettingsDialog, ProgressReaderSettingsPanel)

	def chooseGesture(self, gesture):
		return gesture

	def _parseValue(self, value):
		try:
			if isinstance(value, str):
				match = re.search(r"(\d+\.?\d*)", value.replace(",", "."))
				return float(match.group(1)) if match else 0.0
			return float(value)
		except Exception:
			return 0.0

	def _collectProgressTexts_from_objects(self, objs):
		"""Collects progress reports from a list of NVDA objects."""
		messages = []
		for obj in objs:
			try:
				# First try existing textual description
				name = getattr(obj, "name", None)
				if name and "%" in name:
					messages.append(name)
					continue

				# UIA / IAccessible / check direct attributes as before
				current = self._parseValue(
					getattr(
						obj,
						'value',
						getattr(obj, 'IAccessibleObject', None)
						and getattr(obj.IAccessibleObject, 'accValue', lambda x: "0")(0)
						or 0
					)
				)

				maxValue = self._parseValue(
					getattr(
						obj,
						'maxValue',
						getattr(obj, 'IAccessibleObject', None)
						and getattr(obj.IAccessibleObject, 'accMaximum', lambda x: "100")(0)
						or 100
					)
				)

				if maxValue <= 0:
					maxValue = 100
				if current < 0:
					current = 0

				percent = (current / maxValue) * 100 if maxValue else 0
				percent = max(0.0, min(100.0, percent))

				status = ""
				if hasattr(obj, 'states'):
					if controlTypes.State.BUSY in obj.states:
						status = _(" (aktiv)")
					elif controlTypes.State.UNAVAILABLE in obj.states:
						status = _(" (inaktiv)")

				messages.append(_("{percent}% Fortschritt {status}").format(
					percent=round(percent, 1),
					status=status
				))
			except Exception:
				# continue with next element
				continue
		return messages

	def _collectProgressTexts(self):
		"""Collect progress reports. Use saved objects, if available."""
		# If there are any saved objects, use them.
		if self.rememberedProgressObjects:
			# Filter out destroyed/invalidated objects (ensure that attributes still exist)
			valid_objs = []
			for o in self.rememberedProgressObjects:
				try:
					# A simple access test
					_ = getattr(o, "role", None)
					valid_objs.append(o)
				except Exception:
					continue
			if valid_objs:
				return self._collectProgressTexts_from_objects(valid_objs)

		# If there are no marked objects, search for visible progress bars as before.
		progressBars = self._findProgressBars()
		messages = []
		for progressBar, progressText in progressBars:
			if progressText:
				messages.append(progressText)
				continue

			try:
				current = self._parseValue(
					getattr(
						progressBar,
						'value',
						getattr(progressBar, 'IAccessibleObject', None)
						and getattr(progressBar.IAccessibleObject, 'accValue', lambda x: "0")(0)
						or 0
					)
				)

				maxValue = self._parseValue(
					getattr(
						progressBar,
						'maxValue',
						getattr(progressBar, 'IAccessibleObject', None)
						and getattr(progressBar.IAccessibleObject, 'accMaximum', lambda x: "100")(0)
						or 100
					)
				)

				if maxValue <= 0:
					maxValue = 100
				if current < 0:
					current = 0

				percent = (current / maxValue) * 100 if maxValue else 0
				percent = max(0.0, min(100.0, percent))

				status = ""
				if hasattr(progressBar, 'states'):
					if controlTypes.State.BUSY in progressBar.states:
						status = _(" (aktiv)")
					elif controlTypes.State.UNAVAILABLE in progressBar.states:
						status = _(" (inaktiv)")

				messages.append(_("{percent}% Fortschritt {status}").format(
					percent=round(percent, 1),
					status=status
				))
			except Exception:
				continue
		return messages

	def _updateProgressWindow(self, evt=None):
		try:
			messages = self._collectProgressTexts()
			if messages:
				text = "\n".join(messages)
			else:
				text = _("Keine Progressbar gefunden")
			if self.refreshText:
				# set the text, make it read-only, set the cursor and focus to the first line
				try:
					self.refreshText.SetEditable(True)
				except Exception:
					pass
				try:
					self.refreshText.SetValue(text)
				except Exception:
					try:
						self.refreshText.SetLabel(text)
					except Exception:
						pass
				try:
					self.refreshText.SetInsertionPoint(0)
					self.refreshText.ShowPosition(0)
				except Exception:
					try:
						self.refreshText.SetSelection(0, 0)
					except Exception:
						pass
				try:
					self.refreshText.SetEditable(False)
				except Exception:
					pass
				try:
					# Set focus on TextCtrl
					self.refreshText.SetFocus()
				except Exception:
					pass
		except Exception as e:
			if self.refreshText:
				try:
					self.refreshText.SetValue(_("Fehler beim Auslesen: {}").format(str(e)))
					self.refreshText.SetInsertionPoint(0)
					self.refreshText.SetEditable(False)
					self.refreshText.SetFocus()
				except Exception:
					pass

	def _startAutoRefresh(self):
		interval = int(GlobalPlugin.refreshInterval)
		if self.refreshTimer:
			self.refreshTimer.Stop()
		self.refreshTimer = wx.Timer(self.refreshFrame)
		self.refreshFrame.Bind(wx.EVT_TIMER, self._updateProgressWindow, self.refreshTimer)
		try:
			self.refreshTimer.Start(interval)
		except Exception:
			self.refreshTimer.Start(DEFAULT_INTERVAL_MS)

	def _stopAutoRefresh(self):
		if self.refreshTimer:
			self.refreshTimer.Stop()
			self.refreshTimer = None

	@script(
		description=_("Öffnet ein Fenster mit automatischer Aktualisierung der Progressbar (merkt beim Öffnen gefundene Progress-Objekte)"),
		gesture="kb:NVDA+Shift+R",
		category=_("Progress Reader")
	)
	def script_openRefreshWindow(self, gesture):
		# Toggle: If the window is already open, close it.
		if self.refreshFrame:
			self._stopAutoRefresh()
			try:
				self.refreshFrame.Destroy()
			except Exception:
				pass
			self.refreshFrame = None
			ui.message(_("Auto-Refresh Fenster geschlossen"))
			return

		# Automatically remember currently found Progress objects when opening
		try:
			found = self._findProgressBars()
			objs = [pb for pb, txt in found]
			unique = []
			seen = set()
			for o in objs:
				try:
					uid = (getattr(o, "name", None), getattr(o, "role", None), getattr(o, "windowClassName", None))
					if uid not in seen:
						seen.add(uid)
						unique.append(o)
				except Exception:
					continue
			self.rememberedProgressObjects = unique
			self.rememberingActive = True if unique else False
			if unique:
				ui.message(_("{} Progress-Objekt(e) gemerkt").format(len(unique)))
			else:
				ui.message(_("Keine Progress-Objekte gefunden zum Merken"))
		except Exception:
			ui.message(_("Fehler beim Merken der Progress-Objekte"))

		# Create the window with TextCtrl
		self.refreshFrame = wx.Frame(None, title=_("Progress Reader"), size=(480, 320))
		panel = wx.Panel(self.refreshFrame)
		vbox = wx.BoxSizer(wx.VERTICAL)

		# Multi-line read-only TextCtrl, fills the space
		style = wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_SUNKEN | wx.HSCROLL
		try:
			self.refreshText = wx.TextCtrl(panel, value=_("Lade Fortschritt..."), style=style)
		except Exception:
			self.refreshText = wx.TextCtrl(panel, value=_("Lade Fortschritt..."), style=wx.TE_MULTILINE | wx.TE_READONLY)

		vbox.Add(self.refreshText, 1, wx.EXPAND | wx.ALL, 12)

		panel.SetSizer(vbox)
		self.refreshFrame.Show()

		# Try to set focus to TextCtrl immediately
		try:
			self.refreshText.SetFocus()
			try:
				self.refreshText.SetInsertionPoint(0)
				self.refreshText.ShowPosition(0)
			except Exception:
				try:
					self.refreshText.SetSelection(0, 0)
				except Exception:
					pass
		except Exception:
			pass

		# Update immediately and start timer
		self._updateProgressWindow()
		self._startAutoRefresh()

		def onClose(evt):
			self._stopAutoRefresh()
			try:
				self.refreshFrame.Destroy()
			except Exception:
				pass
			self.refreshFrame = None
			evt.Skip()
		self.refreshFrame.Bind(wx.EVT_CLOSE, onClose)

	@script(
		description=_("Setzt das Aktualisierungsintervall für das Auto-Refresh-Fenster"),
		gesture="kb:NVDA+Shift+U",
		category=_("Progress Reader")
	)
	def script_setInterval(self, gesture):
		# Open the dialog safely on the GUI thread and with the NVDA main window as the parent
		def _showIntervalDialog():
			dlg = wx.TextEntryDialog(gui.mainFrame, _("Neues Intervall in Sekunden:"), _("Intervall einstellen"))
			try:
				if dlg.ShowModal() == wx.ID_OK:
					val = dlg.GetValue()
					try:
						newSeconds = int(val)
						if newSeconds <= 0:
							raise ValueError("non-positive")
						newVal = newSeconds * 1000
						GlobalPlugin.refreshInterval = newVal
						_setConfigInterval(newVal)
						ui.message(_("Intervall gesetzt auf {} ms").format(newVal))
						if self.refreshFrame:
							self._startAutoRefresh()
					except Exception:
						ui.message(_("Ungültige Eingabe"))
			finally:
				try:
					dlg.Destroy()
				except Exception:
					pass

		try:
			wx.CallAfter(_showIntervalDialog)
		except Exception:
			# Fallback: call directly
			_showIntervalDialog()

	def _findProgressBars(self):
		"""
Searches the current foreground hierarchy for progress bars, as before.
		Returns a list of (obj, text) tuples.
		"""
		q = Queue()
		root = api.getForegroundObject()
		q.put(root)
		progressBars = []
		while not q.empty():
			obj = q.get()
			try:
				if obj.windowClassName == "OperationStatusWindow":
					name = getattr(obj, 'name', '')
					if name and "%" in name:
						progressBars.append((obj, name))
					for child in obj.children:
						if hasattr(child, "UIAElement") and child.UIAElement:
							if child.UIAElement.controlType == UIAHandler.UIA_ControlTypeIds.PROGRESSBAR:
								if child.value is not None:
									progressBars.append((child, str(child.value)))
						if hasattr(child, 'IAccessibleObject') and child.IAccessibleObject:
							try:
								if child.IAccessibleObject.accRole(0) == controlTypes.Role.PROGRESSBAR:
									val = child.IAccessibleObject.accValue(0)
									if val and "%" in val:
										progressBars.append((child, val))
							except Exception:
								pass
				if hasattr(obj, 'UIAElement') and obj.UIAElement:
					if obj.UIAElement.controlType == UIAHandler.UIA_ControlTypeIds.PROGRESSBAR:
						if obj.value is not None:
							progressBars.append((obj, str(obj.value)))
				if hasattr(obj, 'IAccessibleObject') and obj.IAccessibleObject:
					try:
						if obj.IAccessibleObject.accRole(0) == controlTypes.Role.PROGRESSBAR:
							val = obj.IAccessibleObject.accValue(0)
							if val and "%" in val:
								progressBars.append((obj, val))
					except Exception:
						pass
				if getattr(obj, "role", None) == controlTypes.ROLE_PROGRESSBAR:
					if getattr(obj, "value", None) is not None:
						progressBars.append((obj, str(obj.value)))
				if hasattr(obj, "value") and hasattr(obj, "maxValue"):
					try:
						if obj.value > 0:
							progressBars.append((obj, str(obj.value)))
					except Exception:
						pass
				for child in getattr(obj, 'children', []):
					q.put(child)
			except Exception:
				continue
		return progressBars if progressBars else []
