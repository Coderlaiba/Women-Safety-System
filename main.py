import threading
import time
import location_service
import sms_service
import database

class CoreEmergencyPipelineCoordinator:
    def __init__(self):
        self.is_emergency_active = False
        self.pipeline_mutex_lock = threading.Lock()
        self.gui_ui_callback = None  # GUI window register karne ke liye

    def route_incident_trigger(self, source_origin, gui_callback=None):
        if gui_callback:
            self.gui_ui_callback = gui_callback

        with self.pipeline_mutex_lock:
            if source_origin == "MANUAL_PANIC_SOS":
                print("🚨 PRIORITY OVERRIDE: Manual Button Clicked!")
                self.is_emergency_active = True
                self.dispatch_global_protocols(self.gui_ui_callback)
                return

            if source_origin == "BACKGROUND_VOICE_MIC" and not self.is_emergency_active:
                print("🎤 Triggered via Mic Voice.")
                self.is_emergency_active = True
                # Yahan saved gui_ui_callback pass kar rahe hain taaki screen par dikhe
                self.dispatch_global_protocols(self.gui_ui_callback)

    def dispatch_global_protocols(self, gui_callback):
        try:
            # GUI screen par immediate alert update text bhejein
            if gui_callback:
                gui_callback("🚨 [VOICE TRIGGER] Safety code word detected! Processing...")

            # 1. Hardware Location Tracer Engine
            map_url, city = location_service.get_live_location()
            
            # Screen par real-time updates/link output render karein
            if gui_callback:
                gui_callback(f"[📍 LOCATION] Found: {city}\n👉 Link: {map_url}")
                
            print(f"📍 Center Resolved: {city} | URL: {map_url}")
            
            # 2. Database contact lookup arrays
            raw_contacts = database.fetch_all_active_contacts()
            
            if not raw_contacts:
                print("❌ No contacts found inside Database.")
                if gui_callback:
                    gui_callback("❌ Alert target numbers empty inside Database.")
                return
                
            # 3. Dispatched notifications log trace
            if gui_callback:
                gui_callback(f"📱 Forwarding emergency SMS logs to guardians...")
                
            sms_service.send_emergency_sms(raw_contacts, map_url)
            
            if gui_callback:
                gui_callback("✅ Signals successfully transmitted to all guardians!")
            
        except Exception as e:
            print(f"🚨 System Error: {e}")
            if gui_callback:
                gui_callback(f"🚨 System Error: {e}")
        finally:
            time.sleep(5)
            self.is_emergency_active = False

system_coordinator = CoreEmergencyPipelineCoordinator()

def deploy_audio_pipeline_safely(system_manager_instance, contacts_callback):
    try:
        import audio_service
        audio_service.deploy_audio_pipeline_safely(
            system_coordinator=system_manager_instance,
            fetch_contacts_callback=contacts_callback
        )
    except Exception as hardware_crash:
        print(f"⚠️ MIC HARDWARE OFFLINE: {hardware_crash}")