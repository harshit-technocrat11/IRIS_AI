window.addEventListener("DOMContentLoaded", () => {
  const tg = window.Telegram?.WebApp;
  if (tg) tg.expand();

  let room;

  async function initCall() {
    const LiveKit = window.LivekitClient || window.LiveKit;

    if (!LiveKit) {
      document.getElementById("status").innerText = "SDK Loading Error";
      console.error(
        "LiveKit CDN script failed to load into window.LivekitClient",
      );
      return;
    }

    try {
      const userId = tg?.initDataUnsafe?.user?.id || "local_user";
      const res = await fetch(
        `/api/livekit-token?room=iris-room&identity=user_${userId}`,
      );
      const data = await res.json();

      if (!res.ok || !data.token) {
        throw new Error(data.detail || "Failed to fetch WebRTC token");
      }

      const { token, url } = data;

      room = new LiveKit.Room();

      // Subscribe to IRIS AI incoming audio track
      room.on(LiveKit.RoomEvent.TrackSubscribed, (track) => {
        if (track.kind === LiveKit.Track.Kind.Audio) {
          const audioElem = track.attach();
          document.body.appendChild(audioElem);
        }
      });

      await room.connect(url, token);

      await room.localParticipant.setMicrophoneEnabled(true);

      document.getElementById("status").innerText = "🎙️ Connected to IRIS";
    } catch (err) {
      document.getElementById("status").innerText = "Connection Failed";
      console.error("initCall error:", err);
    }
  }

  document.getElementById("endBtn").onclick = () => {
    if (room) room.disconnect();
    if (tg) tg.close();
  };

  initCall();
});
