import cantools
import os

class DBCDecoder:
    def __init__(self, dbc_files):

        project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.db = cantools.database.Database()

        for f in dbc_files:
            full_path = os.path.join(project_root, f)
            self.db.add_dbc_file(full_path)

        print(f"Total de mensagens carregadas: {len(self.db.messages)}")

        ids = {}
        for msg in self.db.messages:
            if msg.frame_id in ids:
                print(f"⚠️ ID duplicado: 0x{msg.frame_id:X} ({msg.name} / {ids[msg.frame_id]})")
            else:
                ids[msg.frame_id] = msg.name

    def decode(self, msg):
        try:
            msg_def = self.db.get_message_by_frame_id(msg.arbitration_id)
            decoded = msg_def.decode(msg.data)
            return msg_def.name, decoded
        except:
            return None, None

    def encode(self, message_name, signals):
        msg = self.db.get_message_by_name(message_name)
        return msg.frame_id, msg.encode(signals)
