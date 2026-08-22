# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (318)

```
 10827  GET              /                                                dashboard
 16577  GET              /api/abo/status                                  api_abo_status
 10926  GET              /api/active-recordings                           api_active_recordings
 16652  GET              /api/activity-pulse                              api_activity_pulse
 15686  GET              /api/ai-log                                      api_ai_log
 11324  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 26058  GET              /api/ai/anomalies                                api_ai_anomalies
 13065  POST             /api/ai/ask                                      api_ai_ask
 13316  GET              /api/ai/config                                   api_freeai_status
 11503  GET              /api/ai/conversations                            api_ai_conversations_list
 11514  POST             /api/ai/conversations                            api_ai_conversations_create
 11524  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get
 11547  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete
 11554  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch
 11565  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send
 11698  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream
 12367  POST             /api/ai/diagnose                                 api_ai_diagnose
 26296  GET              /api/ai/forecast-storage                         api_ai_forecast_storage
 26330  GET              /api/ai/health-score/<username>                  api_ai_health_score
 11487  GET              /api/ai/models                                   api_ai_models
 26011  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive
 25991  POST             /api/ai/query                                    api_ai_query
 26164  GET              /api/ai/recommendations                          api_ai_recommendations
 26212  GET              /api/ai/report                                   api_ai_report
 26263  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice
 26122  GET              /api/ai/segments                                 api_ai_segments
 25966  GET              /api/ai/skills                                   api_ai_skills
 16379  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 15731  GET              /api/archive                                     api_archive
 16027  DELETE           /api/archive/<int:eid>                           api_archive_delete
 15886  POST             /api/archive/<int:eid>/rename                    api_archive_rename
 15864  POST             /api/archive/bulk-delete                         api_archive_bulk_delete
 15854  GET              /api/archive/check                               api_archive_check
 12474  GET              /api/archive/duplicates                          api_archive_duplicates
 12490  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete
 15919  POST             /api/archive/upload                              api_archive_upload
 24386  GET/POST         /api/audio/config                                api_audio_config
 24416  POST             /api/audio/testtone                              api_audio_testtone
 16485  GET/POST         /api/auto-archive-rules                          api_archive_rules
 16509  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 16513  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 13278  GET              /api/automation/status                           api_automation_status
 13300  POST             /api/automation/toggle                           api_automation_toggle
 14774  GET              /api/azrael/agents                               api_azrael_agents
 13184  POST             /api/azrael/ask                                  api_azrael_ask
 24622  GET/POST         /api/azrael/context                              api_azrael_context
 14431  GET              /api/azrael/core                                 api_azrael_core
 24756  POST             /api/azrael/live_pause                           api_azrael_live_pause
 24746  GET              /api/azrael/live_status                          api_azrael_live_status
 24764  POST             /api/azrael/live_test                            api_azrael_live_test
 14783  GET              /api/azrael/memories                             api_azrael_memories
 24812  POST             /api/azrael/persona                              api_azrael_persona_set
 24803  GET              /api/azrael/personas                             api_azrael_personas
 24840  GET              /api/azrael/piper_status                         api_azrael_piper_status
 24595  POST             /api/azrael/react                                api_azrael_react
 24631  GET              /api/azrael/reaction                             api_azrael_reaction
 24783  GET              /api/azrael/reactions                            api_azrael_reactions
 24833  GET              /api/azrael/transcript                           api_azrael_transcript
 24718  POST             /api/azrael/tts_test                             api_azrael_tts_test
 24693  GET              /api/azrael/voices                               api_azrael_voices
 24857  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11885  GET              /api/backoff-watch                               api_backoff_watch
 15377  POST             /api/backup/run                                  api_backup_run
 15343  GET              /api/backup/status                               api_backup_status
 15332  POST             /api/backup/system                               api_backup_system
 16451  GET              /api/bandwidth/live                              api_bandwidth_live
 16346  GET              /api/bookmarks                                   api_bookmarks_list
 12148  GET              /api/brain                                       api_brain
 12085  GET              /api/brain/alarms                                api_brain_alarms
 12070  GET              /api/brain/creator                               api_brain_creator
 12047  GET              /api/brain/graph                                 api_brain_graph
 12108  GET              /api/brain/growth                                api_brain_growth
 25320  GET              /api/channel/categories                          api_channel_categories
 25326  POST             /api/channel/set                                 api_channel_set
 25136  GET              /api/channels/status                             api_channels_status
 24159  POST             /api/chat/send                                   api_chat_send
 10907  GET              /api/checks                                      api_checks
 24659  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 24642  GET              /api/clips                                       api_clips
 24675  POST/DELETE      /api/clips/clear                                 api_clips_clear
 17380  GET/POST         /api/collections                                 api_collections
 17415  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify
 17479  GET              /api/collections/<int:cid>/trackings             api_collection_trackings
 17820  GET              /api/community/stats                             api_community_stats
 26836  POST             /api/config/restore                              api_config_restore
 26821  GET              /api/config/snapshot                             api_config_snapshot
 16720  GET              /api/cookies/age                                 api_cookies_age
 10974  GET              /api/cookies/health                              api_cookies_health
 10981  POST             /api/cookies/update                              api_cookies_update
 26787  GET              /api/data/export                                 api_data_export
 18240  GET              /api/db/export                                   api_db_export
 18267  POST             /api/db/import                                   api_db_import
 18227  GET              /api/db/summary                                  api_db_summary
 27744  GET              /api/defense/attacks                             api_defense_attacks
 27729  GET              /api/defense/fail2ban                            api_defense_fail2ban
 27453  GET              /api/defense/overview                            api_defense_overview
 15439  POST             /api/discord/announce                            api_discord_announce
 15141  GET              /api/discord/clips_week                          api_discord_clips_week
 15383  GET              /api/discord/community                           api_discord_community
 14551  GET              /api/discord/overview                            api_discord_overview
 14637  POST             /api/discord/webhook_test                        api_discord_webhook_test
 17833  GET              /api/donations/summary                           api_donations_summary
 16433  GET              /api/events                                      api_events
 15188  GET              /api/events/stream                               api_events_stream
 18895  GET              /api/evolution/changelog                         api_evolution_changelog
 18880  GET              /api/evolution/history                           api_evolution_history
 18820  GET              /api/evolution/learned                           api_evolution_learned
 18842  GET              /api/evolution/proposals                         api_evolution_proposals
 18863  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 18810  POST             /api/evolution/run                               api_evolution_run
 18910  GET              /api/evolution/snapshots                         api_evolution_snapshots
 18775  GET              /api/evolution/status                            api_evolution_status
 18043  GET              /api/finanzamt/entries                           api_finanzamt_entries
 18063  POST             /api/finanzamt/entry                             api_finanzamt_add
 18090  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 16446  GET              /api/forecast/storage                            api_forecast_storage
 14504  GET              /api/health                                      api_health
 11803  GET              /api/health-score                                api_health_score
 16464  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 16460  GET              /api/heatmap/recordings                          api_heatmap_recordings
 24310  GET              /api/highlights                                  api_highlights
 24322  POST             /api/highlights/config                           api_highlights_config
 17185  GET              /api/insights/activity-clock                     api_insights_activity_clock
 17060  GET              /api/insights/best-times/<username>              api_insights_best_times
 17167  GET              /api/insights/catch-rate                         api_insights_catch_rate
 17142  GET              /api/insights/growth/<username>                  api_insights_growth
 17206  GET              /api/insights/leaderboard                        api_insights_leaderboard
 17093  GET              /api/insights/reliability                        api_insights_reliability
 17116  GET              /api/insights/session-stats                      api_insights_session_stats
 17240  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer
 25177  GET              /api/kick/channel                                api_kick_channel
 25198  POST             /api/kick/channel                                api_kick_channel_set
 14274  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 14315  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 14259  GET              /api/kick/oauth/start                            api_kick_oauth_start
 14299  GET              /api/kick/oauth/status                           api_kick_oauth_status
 24434  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 24503  POST             /api/kickmod/config                              api_kickmod_config
 24548  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 24562  GET              /api/kickmod/learned                             api_kickmod_learned
 24589  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 24569  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 24900  POST             /api/kickmod/say                                 api_kickmod_say
 24876  POST             /api/kickmod/start                               api_kickmod_start
 24474  GET              /api/kickmod/status                              api_kickmod_status
 24887  POST             /api/kickmod/stop                                api_kickmod_stop
 17805  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13744  POST             /api/marketing/config                            api_marketing_config
 13769  GET              /api/marketing/preview                           api_marketing_preview
 13779  POST             /api/marketing/send-now                          api_marketing_send_now
 13718  GET              /api/marketing/status                            api_marketing_status
 13736  POST             /api/marketing/toggle                            api_marketing_toggle
 24337  GET              /api/moderation/feed                             api_moderation_feed
 14120  POST             /api/news/config                                 api_news_config
 14162  POST             /api/news/generate-now                           api_news_generate_now
 14157  GET              /api/news/items                                  api_news_items
 14148  GET              /api/news/preview                                api_news_preview
 14099  GET              /api/news/status                                 api_news_status
 14112  POST             /api/news/toggle                                 api_news_toggle
 17662  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 15006  GET              /api/notify/status                               api_notify_status
 15017  POST             /api/notify/test                                 api_notify_test
 14992  GET              /api/ops/audit                                   api_ops_audit
 17733  GET              /api/ops/db-stats                                api_ops_db_stats
 17761  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14798  GET              /api/ops/errors                                  api_ops_errors
 17682  GET              /api/ops/healthcheck                             api_ops_healthcheck
 18322  GET              /api/ops/log-tail                                api_ops_log_tail
 13164  GET              /api/ops/logtail                                 api_ops_logtail
 14739  GET              /api/ops/metrics                                 api_ops_metrics
 18296  GET              /api/ops/version                                 api_ops_version
 11177  GET              /api/outcomes                                    api_outcomes
 25817  POST             /api/overlay/config                              api_overlay_config
 25804  POST             /api/overlay/event                               api_overlay_event
 25709  GET              /api/overlay/state                               api_overlay_state
 11210  GET              /api/profile/<username>                          api_profile
 16728  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 16472  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 16631  GET              /api/proxy/heatmap                               api_proxy_heatmap
 16608  GET              /api/proxy/trend                                 api_proxy_trend
 14073  GET              /api/public/stats                                api_public_stats
 10861  GET              /api/pulse                                       api_pulse
 26358  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify
 26442  GET              /api/rec/compress-candidates                     api_rec_compress_candidates
 26501  GET              /api/rec/orphans                                 api_rec_orphans
 26512  POST             /api/rec/orphans/clean                           api_rec_orphans_clean
 26345  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality
 26409  POST             /api/rec/retention/apply                         api_rec_retention_apply
 26396  POST             /api/rec/retention/preview                       api_rec_retention_preview
 26375  GET              /api/rec/timeline/<username>                     api_rec_timeline
 15710  GET              /api/recording-attempts                          api_recording_attempts
 16363  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations
 16358  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark
 16560  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint
 16278  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect
 17328  POST             /api/recordings/<int:rid>/label                  api_recording_label
 16522  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest
 16331  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes
 16304  GET              /api/recordings/<int:rid>/quality                api_recording_quality
 17302  POST             /api/recordings/<int:rid>/rating                 api_recording_rating
 16696  POST             /api/recordings/<int:rid>/restore                api_recording_restore
 17261  POST             /api/recordings/<int:rid>/star                   api_recording_star
 16692  POST             /api/recordings/<int:rid>/trash                  api_recording_trash
 16530  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform
 15587  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop
 17345  GET              /api/recordings/by-label/<label>                 api_recordings_by_label
 16830  POST             /api/recordings/dedup-scan                       api_dedup_scan
 18205  GET              /api/recordings/disconnects                      api_recording_disconnects
 17363  GET              /api/recordings/labels                           api_recordings_labels
 15631  GET              /api/recordings/list                             api_recordings_list
 16687  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop
 16674  GET              /api/recordings/manual/list                      api_manual_list
 16658  POST             /api/recordings/manual/start                     api_manual_start
 16795  GET              /api/recordings/overview                         api_recordings_overview
 17281  GET              /api/recordings/starred                          api_recordings_starred
 16700  GET              /api/recordings/trash                            api_trash_list
 24094  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 24072  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 24113  POST             /api/restream/<int:rid>/start                    api_restream_start
 24257  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 25671  GET              /api/restream/chatfeed                           api_restream_chatfeed
 24048  POST             /api/restream/create                             api_restream_create
 14323  GET              /api/restream/deck                               api_restream_deck
 13252  GET              /api/restream/health                             api_restream_health
 25693  POST             /api/restream/layout                             api_restream_layout
 24021  GET              /api/restream/list                               api_restream_list
 13228  POST             /api/restream/report                             api_restream_report
 24270  POST             /api/restream/start_all                          api_restream_start_all
 24296  POST             /api/restream/stop_all                           api_restream_stop_all
 13492  GET              /api/restream/testpush                           api_testpush_status
 13517  POST             /api/restream/testpush                           api_testpush_run
 17949  GET              /api/restream/verify                             api_restream_verify
 15119  GET              /api/retention/preview                           api_retention_preview
 15128  POST             /api/retention/run                               api_retention_run
 26902  POST             /api/schedule/add                                api_schedule_add
 26892  GET              /api/schedule/list                               api_schedule_list
 26927  POST             /api/schedule/remove                             api_schedule_remove
 15048  POST             /api/scheduler/add                               api_scheduler_add
 15069  POST             /api/scheduler/delete                            api_scheduler_delete
 15035  GET              /api/scheduler/list                              api_scheduler_list
 15080  POST             /api/scheduler/toggle                            api_scheduler_toggle
 16268  GET              /api/search                                      api_search
 27500  GET              /api/selftest                                    api_selftest
 24130  GET              /api/shield/stats                                api_shield_stats
 10880  GET              /api/stats                                       api_stats
 16646  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 16573  GET              /api/stats/tiktok-status                         api_tiktok_status
 26867  GET              /api/stats/timeline                              api_stats_timeline
 10948  GET              /api/storage                                     api_storage
 10955  POST             /api/storage/cleanup                             api_storage_cleanup
 16548  GET              /api/stream/inspect/<username>                   api_stream_inspect
 13205  GET              /api/stream/timeline                             api_stream_timeline
 14625  GET              /api/stream/transcript                           api_stream_transcript
 26535  GET              /api/streamer/compare                            api_streamer_compare
 26734  POST             /api/streamer/delete/<username>                  api_streamer_delete
 15093  GET              /api/streamer/detail                             api_streamer_detail
 26759  GET              /api/streamer/digest/<username>                  api_streamer_digest
 26639  GET              /api/streamer/dormant                            api_streamer_dormant
 26715  GET              /api/streamer/exists/<username>                  api_streamer_exists
 26594  GET              /api/streamer/journal/<username>                 api_streamer_journal
 26559  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 26619  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14471  GET              /api/streamers/wall                              api_streamers_wall
 11097  GET              /api/summary/preview                             api_summary_preview
 16139  GET              /api/system                                      api_system
 16035  GET              /api/system-resources                            api_system_resources
 17897  GET              /api/system/check_timing                         api_check_timing
 18188  GET              /api/system/config_drift                         api_config_drift
 14661  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14853  GET              /api/system/preflight                            api_system_preflight
 14979  GET              /api/system/preflight_history                    api_system_preflight_history
 15279  GET              /api/system/resilience                           api_system_resilience
 16384  GET              /api/tags                                        api_tags_list
 10921  GET              /api/top                                         api_top
 13138  GET              /api/trackings                                   api_trackings
 17450  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 17501  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 16420  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 16711  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 17530  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 16406  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15469  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15516  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 15545  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 15527  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 11114  POST             /api/trackings/bulk                              api_trackings_bulk
 15484  GET              /api/trackings/export                            api_trackings_export
 16388  GET              /api/trackings/tags-map                          api_trackings_tags_map
 16766  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11940  GET              /api/trend-7d                                    api_trend_7d
 24707  GET              /api/tts/<fn>                                    api_tts_file
 13372  POST             /api/tunnel/set                                  api_tunnel_set
 13351  GET              /api/tunnel/status                               api_tunnel_status
 13383  POST             /api/tunnel/test                                 api_tunnel_test
 13364  POST             /api/tunnel/toggle                               api_tunnel_toggle
 18149  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 18126  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 18108  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 25845  GET              /api/upload_window                               api_upload_window
 11191  GET              /api/userstats                                   api_userstats
 14173  GET              /api/version                                     api_version
 17569  GET/POST         /api/webhooks                                    api_webhooks
 17609  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete
 17640  POST             /api/webhooks/<int:wid>/test                     api_webhook_test
 17624  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle
 18005  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 18026  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 17990  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 17974  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 16002  GET              /archive/<int:eid>/download                      archive_download
 16169  GET              /download/<int:recording_id>                     download
 15671  GET              /health                                          health
 24232  GET              /healthz                                         healthz
 10789  GET              /manifest.webmanifest                            pwa_manifest
 14687  GET              /metrics                                         api_prometheus_metrics
 25654  GET              /overlay                                         overlay_page
 10813  GET              /pwa-icon-<variant>.png                          pwa_icon
 10799  GET              /sw.js                                           pwa_service_worker
```

## Discord-Slash-Commands (45)

```
 28091  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 28550  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 28182  /assign_role            Rolle/Gruppe einem Mitglied geben
 28228  /ban                    Mitglied bannen
 28882  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 28806  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 28846  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 28831  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 28673  /clips                  Letzte Highlight-Clips eines Users
 28143  /create_category        Kategorie anlegen
 28112  /create_channel         Text-Channel anlegen (optional in Kategorie)
 28171  /create_group           Nutzergruppe (= Rolle) anlegen
 28154  /create_role            Rolle / Nutzergruppe anlegen
 28128  /create_voice           Voice-Channel anlegen
 28464  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 28580  /event                  Community-Event ankündigen (Admin) — mit Countdown
 28623  /events                 Kommende Community-Events anzeigen
 28719  /follow                 Bei Live-Gang eines Streamers gepingt werden
 28703  /help                   Alle Bot-Befehle anzeigen
 28217  /kick                   Mitglied kicken
 28446  /leaderboard            Top-10 der Community nach XP
 28659  /livenow                Welche getrackten User sind gerade live
 28689  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 28520  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 28252  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 28432  /rank                   Dein Level und Rang anzeigen
 28646  /recstatus              Aktuell laufende Aufnahmen
 28193  /remove_role            Rolle/Gruppe entfernen
 28105  /restream_status        Restream-Status
 28204  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 28397  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 28415  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 28745  /stats                  Statistik zu einem getrackten Streamer
 28017  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 29041  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 28938  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 28914  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 28239  /timeout                Mitglied stummschalten (Minuten)
 28817  /topstreamers           Rangliste der Streamer nach Aufnahmen
 28047  /track                  TikTok-User tracken
 28031  /tracklist              Getrackte TikTok-User dieses Servers
 28734  /unfollow               Live-Pings für einen Streamer abbestellen
 28080  /untrack                TikTok-User nicht mehr tracken
 28767  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 28791  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 29525  on_member_join
 29487  on_message
 29128  on_raw_reaction_add
 29560  on_ready
```

## Top-Level-Symbole in bot_v37.py (520 Funktionen, 2 Klassen)

```
  2437-2438   _abo_key
  2490-2508   _abo_probe_dump
 27002-27012  _active_recorder_sync
 21421-21435  _ad_allowlist
 22523-22529  _agent_for
 27014-27032  _ai_calls_total_sync
 13051-13061  _ai_dashboard_rate_check
 22532-22548  _ai_telemetry
 23007-23025  _alert
 29670-29720  _alert_monitor_loop
  3944-3961   _archive_open_unique
 10637-10655  _arg_int
 19643-19667  _audio_cfg
 23122-23144  _audio_tap_cmd
 10725-10736  _auth_cookie
 10699-10721  _auth_guard
  1475-1480   _auto_on
 23997-24015  _auto_restream_loop
 31166-31181  _azrael_broadcast_reply
 31091-31113  _azrael_chat_reply
 31074-31088  _azrael_chat_should_reply
 31119-31134  _azrael_gate_cfg
 22553-22567  _azrael_live_state
 25537-25551  _azrael_overlay_state
 22903-22944  _azrael_proactive_loop
 22372-22428  _azrael_reaction_to_chats
 31137-31144  _azrael_reply_all_chats
 31061-31071  _azrael_self_names
 31147-31163  _azrael_send_to
 22570-22591  _azrael_system
 29834-29837  _backup_active
 29915-29928  _backup_loop
 21309-21310  _badwords_path
 29635-29644  _brain_growth_loop
 12016-12043  _brain_growth_snapshot
  2373-2393   _brain_hint_delay
 12008-12010  _brain_history_for
  7429-7457   _brain_notify
 11985-12006  _brain_record
 12012-12014  _brain_stream_recent
 15167-15184  _browser_push
 11458-11478  _build_context_for_llm
  7473-7560   _build_daily_summary
  2900-3080   _build_native_cmd
 20010-20192  _build_restream_cmd
  3114-3147   _build_ytdlp_cmd
 26954-26961  _cached_probe
  6224-6251   _can_stop_tracking
  1655-1677   _capture_set_cookies
 16883-16895  _cfg_get
 16898-16920  _cfg_set
 25281-25316  _channel_set_all
 19113-19116  _chat_connected
 19119-19135  _chat_disconnected
  9262-9273   _chat_is_forum
 19175-19177  _chat_sanitize
 19179-19188  _chat_src_ok
 19098-19110  _chat_stat
 19138-19161  _chat_stats_snapshot
  3701-3712   _check_ai_alive_sync
  3715-3727   _check_ai_models_sync
 26963-26976  _check_redis_alive_sync
 26978-26998  _check_redis_version_sync
 12746-12789  _classify_pool_anonymity
 12792-12809  _classify_pool_anonymity_bg
 10677-10684  _client_ip
 30218-30222  _clip_caption_escape
 30164-30191  _clip_prune
 30194-30204  _clip_recfile_for
 30739-30745  _clip_should_velocity
 30263-30346  _clip_to_discord
  3560-3569   _close_ai_session
 30395-30429  _community_events_loop
 11401-11437  _conv_add_message
 11440-11445  _conv_archive
 11369-11378  _conv_create
 11383-11398  _conv_messages
 11448-11455  _conv_rename
  7853-7893   _cookie_alarm_loop
  1727-1731   _cookie_autorefresh_info
  1632-1636   _cookie_header
 15217-15275  _cpu_load_snapshot
  3897-3909   _create_index_safe
 27255-27361  _crowdsec_status
 27221-27252  _crowdsec_via_lapi
 27046-27065  _cscli_bin
 27071-27084  _cscli_path
  7746-7771   _daily_summary_loop
 27102-27120  _darf_journal_lesen
 29647-29667  _db_maintenance_loop
  7718-7743   _db_vacuum_loop
 21451-21475  _detect_foreign_ad
  1232-1243   _diag_path_owner
 22809-22853  _director_finalize
 23568-23575  _director_for
 22758-22806  _director_mark
 30633-30668  _disc_automod_check
 30606-30612  _disc_state_get
 30615-30622  _disc_state_set
 30567-30603  _discord_live_thread
 22947-22959  _discord_notify
 27855-27880  _discord_ops_alert
 30465-30563  _discord_post_user
 27954-29632  _discord_run_once
 27893-27951  _discord_start
 30135-30141  _discord_stop
  7774-7848   _disk_alarm_loop
 32260-32309  _disk_autoclean
 32312-32325  _disk_guard_loop
 32252-32257  _disk_pct
 25594-25613  _donations_unknown_count
 19505-19541  _drawtext_chain
 12671-12735  _enrich_proxies_with_geo
  1872-1916   _ensure_cookie_file_netscape
 30360-30392  _ensure_error_channel
 12914-12951  _ensure_proxy_ready
  9275-9298   _ensure_topic
   599-611    _env_int
   614-629    _env_int_range
 30432-30462  _error_channel_loop
 22991-23004  _event_webhook
 18383-18389  _evo_build_dir
 18392-18399  _evo_version
 18675-18756  _evolution_cycle
 18408-18428  _evolution_llm_note
 18759-18769  _evolution_loop
 18431-18672  _evolution_write_build
  6844-6905   _extract_file_payload
  2048-2095   _extract_urls_from_streamurl_node
 27087-27094  _f2b_sudo_hint
 23027-23029  _faster_whisper_available
 21333-21345  _fetch_ldnoobw_de
 12560-12578  _fetch_proxy_list
 23402-23430  _fetch_tiktok_room_id
   688-704    _ff_cmd
 17040-17054  _ffmpeg_version_str
 30207-30215  _ffprobe_duration
 19782-19787  _find_chromium
  3107-3111   _find_external_recorder
 26469-26497  _find_orphans
  2098-2129   _find_stream_urls
 16963-16988  _fire_webhooks
 27176-27218  _geo_lookup_ips
  3549-3558   _get_ai_session
  8463-8503   _get_live_info
  2687-2694   _get_resolve_semaphore
  8642-8989   _handle_single_tracking
 32170-32172  _hb
 32175-32192  _hb_while
 19193-19211  _highlight_cfg
 19214-19240  _highlight_observe
 19790-19795  _htmlov_screenshot_cmd
 23146-23156  _httpx_proxy
 17001-17013  _in_quiet_hours
 33000-33031  _install_fast_eventloop
 10537-10586  _install_fast_json
  6213-6222   _is_authorized
  8572-8578   _is_dead
  1994-1998   _is_hevc
 27123-27129  _is_private_ip
  1378-1385   _is_process_running
  7459-7470   _is_quiet_hours
  1040-1049   _is_upload_window
 10621-10634  _json_error_handler
 30094-30132  _kick_announce_loop
  7676-7706   _kick_broadcaster_id
 13418-13437  _kick_channel_live
  7593-7635   _kick_follower_count
 14227-14240  _kick_oauth_exchange
 14243-14255  _kick_oauth_page
 14188-14190  _kick_redirect_uri
  7578-7580   _kick_slug
 14193-14224  _kick_user_token
  3967-3975   _kind_from_filename
 17030-17035  _latest_popularity
 21355-21361  _learned_load
 21352-21353  _learned_path
 21363-21371  _learned_save
 23783-23813  _live_react_loop
 23579-23772  _live_react_worker
 22431-22442  _live_transcript_push
 23774-23781  _live_users
 22856-22900  _living_title_loop
  3599-3609   _llm_list_models
 21312-21320  _load_banned_words_file
  1553-1626   _load_cookies_dict
 29840-29912  _local_backup_scan
 10603-10617  _log_5xx
 20226-20230  _looks_like_codec_err
 20195-20223  _looks_like_source_expired
  8535-8565   _loop_fehler
 16254-16257  _loop_not_ready
 22311-22325  _loyalty_add
 22302-22308  _loyalty_get
 22328-22336  _loyalty_top
  8580-8581   _mark_dead
 13585-13614  _marketing_cfg
 13576-13582  _marketing_default_targets
 13571-13573  _marketing_enabled
 13628-13643  _marketing_flavor
 13698-13714  _marketing_loop
 13646-13656  _marketing_post_discord
 13659-13671  _marketing_post_telegram
 13674-13695  _marketing_publish
 13617-13621  _marketing_state_obj
 13624-13625  _marketing_state_save
 32411-32435  _maybe_hype_clip
  3864-3887   _migrate_columns
 31306-31319  _mod_is_exempt
 31322-31327  _mod_warn_first
 31330-31333  _mod_warn_text
 18938-18946  _modlog
   847-849    _multistream_targets
 13809-13825  _news_cfg
 13796-13798  _news_enabled
 13863-13904  _news_facts
 13931-13953  _news_generate
 14078-14095  _news_loop
 13801-13806  _news_output_path
 13907-13928  _news_phrase
 13838-13845  _news_read
 13828-13831  _news_state_obj
 13834-13835  _news_state_save
 13848-13860  _news_write
 25938-25962  _nl_to_sql
 18974-19001  _normalize_ingest
  2304-2321   _note_check_duration
 22457-22465  _oracle_memories
 22713-22747  _oracle_memorize
 22468-22481  _oracle_persona
 22450-22454  _oracle_recent_text
 19331-19339  _ov_atomic_write
 19319-19325  _ov_bar
 21268-21280  _ov_clip_text
 19328-19329  _ov_oneline
 25621-25650  _overlay_push
 19736-19779  _overlay_render_size
 19060-19064  _overlay_session_reset
 25553-25556  _overlay_src_ok
 21438-21448  _own_invites
 19731-19733  _parse_size
 27369-27449  _parse_ssh_attacks
  8065-8098   _pause_resume_cmd
  1681-1725   _persist_refreshed_cookies
  1519-1551   _pick_checked_pull_proxy
 25443-25445  _piper_available
 25408-25430  _piper_list_voices
 25450-25475  _piper_pick_model
 25487-25534  _piper_say
 25401-25405  _piper_voice_roots
 16925-16960  _post_json_threaded
 19710-19728  _probe_video_size
  1406-1423   _proc_is_recorder
 12658-12669  _proxy_geo_cache_put
 12885-12911  _proxy_pool_refresh_loop
  1485-1516   _proxy_report_recording
 13956-14030  _public_stats
 22962-22988  _push_notify
 10783-10785  _pwa_dir
 12629-12644  _quick_validate_proxy
 16991-16998  _quiet_hours_config
 10748-10781  _rate_guard
 22276-22282  _react_warn
  2344-2366   _record_check_outcome
   664-685    _redact_stream_urls
 12812-12882  _refresh_proxy_pool
 25433-25439  _resolve_piper_model
  2138-2228   _resolve_via_html
  2510-2664   _resolve_via_webcast_api_v2
  2727-2789   _resolve_via_ytdlp
 30785-30914  _resolve_youtube_ingest
 23852-23859  _restream_active_platforms
 19045-19056  _restream_active_sources
 23433-23532  _restream_chat_guardian
 19243-19315  _restream_chat_push
 18949-18959  _restream_enabled
 19798-19885  _restream_html_overlay_start
 19888-19901  _restream_html_overlay_stop
   988-990    _restream_layout_mode
 19010-19033  _restream_overlay_files
 23817-23849  _restream_platform_state
 23959-23994  _restream_resume_after_restart
 19949-20007  _restream_tts_enqueue_wav
 19672-19704  _restream_tts_feeder
 19669-19670  _restream_tts_fifo_path
 19904-19931  _restream_tts_start
 19933-19947  _restream_tts_stop
 23862-23956  _restream_verify_loop
 29805-29817  _retention_loop
 29764-29802  _retention_scan
  2440-2474   _room_is_abo
  6909-7026   _run_ai_call
 16238-16251  _run_async_from_flask
 27132-27173  _run_priv
 32988-32996  _run_selfcheck_and_exit
 29820-29831  _s3_client
 25902-25933  _safe_select
  8583-8629   _safe_send
  5206-5231   _sample_net_throughput
 21322-21330  _save_banned_words_file
  2396-2423   _schedule_next_check
 29723-29761  _scheduler_loop
  3890-3894   _schema_pk
 16259-16264  _scraper_session
 31336-31375  _screen_full
 14520-14546  _sec_headers
  2001-2045   _select_stream_from_data_section
 32839-32985  _selfcheck
  1063-1067   _should_defer_upload
 30225-30260  _shrink_for_discord
 32332-32349  _sign_health_check
 32352-32371  _sign_health_loop
  8516-8527   _spawn
 27493-27496  _st_befund
 23158-23399  _start_chat_listener
 14054-14069  _stats_loop
 14033-14036  _stats_output_path
 14039-14051  _stats_write
  9057-9071   _storage_cleanup_loop
 32391-32398  _story_for
  3169-3175   _stream_url_expiry
  3184-3190   _stream_url_is_fresh
  3177-3182   _stream_url_ttl
 21395-21402  _streamer_persona_get
 21377-21383  _streamer_personas_load
 21374-21375  _streamer_personas_path
 21385-21393  _streamer_personas_save
 19544-19609  _studio_chain
 29937-30059  _system_backup
 30062-30090  _system_backup_loop
 12581-12620  _test_proxy
 13459-13468  _testpush_cfg
 13471-13488  _testpush_exec
 13440-13456  _testpush_resolve_live
  9234-9244   _tg_topics_load_into_mem
  9231-9232   _tg_topics_path
  9246-9253   _tg_topics_save
 26663-26711  _tiktok_account_exists
 10687-10695  _token_ok
  9256-9260   _topic_forget
 17016-17027  _tracking_max_duration
  1290-1313   _try_attach_file_handler
 25477-25485  _tts_cleanup
 13344-13347  _tunnel_effective
 24921-24974  _twitch_channel_status
 31378-31516  _twitch_chat_loop
 31192-31293  _twitch_eventsub_loop
 18170-18184  _twitch_oauth_page
  1086-1099   _upload_queue_add
  1110-1112   _upload_queue_count
  1069-1078   _upload_queue_load
  1059-1061   _upload_queue_path
  1101-1108   _upload_queue_remove
  1080-1084   _upload_queue_save
  1114-1152   _upload_window_loop
 18962-18971  _url_host
  7638-7666   _viewer_sample_loop
  7708-7715   _viewer_stats
 32202-32242  _watchdog_loop
 31040-31048  _wchat_thank_ok
 23031-23058  _whisper_get_model
 23060-23120  _whisper_transcribe
 19341-19503  _write_restream_overlay
 31544-31613  _youtube_api_chat_loop
 24977-25080  _youtube_api_status
 25083-25132  _youtube_channel_status
 31616-31773  _youtube_chat_loop
 30920-30933  _youtube_restream_autoconfig
 30936-30960  _youtube_restream_autoconfig_inner
 31018-31037  _youtube_send
 25237-25278  _youtube_set_channel
 30963-30997  _yt_access_token
 31000-31015  _yt_live_chat_id
 31537-31541  _yt_oauth_configured
 31519-31534  _yt_timeout
  2711-2712   _ytdlp_detect_available
  2714-2725   _ytdlp_note_result
  8399-8423   about
  4345-4364   add_ai_log_entry
  4226-4234   add_archive_entry
  5328-5343   add_archive_rule
  4797-4831   add_recording
  4450-4467   add_tracking
  4900-4917   add_tracking_tag
  7029-7062   ai
  3741-3768   ai_chat
  3802-3812   ai_history_append
  3814-3819   ai_history_clear
  3791-3800   ai_history_load
  3776-3789   ai_rate_limit_check
  7091-7099   aireset
 13328-13339  api_ai_config
  3933-3941   archive_writeable
 22594-22613  azrael_chat
 31778-31900  brain_cmd
  3193-3377   build_recording_cmd
  5799-5845   build_recording_manifest
  4470-4547   bulk_add_trackings
  4031-4071   bulk_delete_archive_entries
  7896-7955   bulkadd
  9074-9214   check_all_trackings
  4634-4650   claim_live_transition
 21478-22221  class KickModerator
 20233-21155  class RestreamManager
 12996-13038  classify_proxy_anonymity
  7137-7335   cleanup
  6073-6114   cleanup_old_recordings
  4788-4795   clear_recording
 30671-30736  clip_moment
  5476-5519   cluster_failures
  5150-5199   compute_storage_forecast
  5953-6019   compute_waveform_peaks
  8018-8062   cookies_cmd
  5848-5854   cookies_days_old
  4441-4447   count_trackings_for_chat
  4332-4343   decide_preferred_recorder
  4244-4268   delete_archive_entry
  5345-5353   delete_archive_rule
  6539-6686   diag
 31903-31964  einnahmen_cmd
  5051-5082   ffprobe_inspect
  5138-5147   find_recordings_by_fingerprint
  4286-4302   finish_recording_attempt
  4579-4589   get_all_active_trackings
  4386-4389   get_all_checks
  4833-4843   get_all_recordings
  4942-4952   get_all_tags_with_counts
  5038-5047   get_annotations_for_recording
  3986-3998   get_archive_aggregate_stats
  4236-4242   get_archive_entry
  4000-4012   get_archive_kind_breakdown
  4015-4029   get_archive_missing_ids
  5023-5034   get_bookmarked_recordings
  1748-1865   get_cookie_health
  4883-4897   get_event_log
  4316-4330   get_last_recording_attempt
  2792-2897   get_live_status
  5679-5689   get_manual_recordings
  5084-5098   get_or_compute_inspect_sync
  6149-6193   get_outcome_breakdown
  4999-5007   get_priority_poll_interval
  5306-5315   get_profile_snapshots
  4366-4376   get_recent_ai_log
  4304-4314   get_recent_recording_attempts
  4845-4847   get_recording_by_id
  5011-5019   get_recording_note
  3497-3520   get_redis
  4417-4433   get_stats
  6040-6071   get_storage_stats
  4932-4940   get_tags_for_tracking
  5446-5460   get_tiktok_status_distribution
  4986-4997   get_tracking_priority
  4652-4665   get_tracking_state
  4575-4577   get_trackings_for_group
  5725-5734   get_trash_recordings
  9918-10519  handle_recording_finished
  3912-3931   init_db
  5896-5950   inspect_stream_url
 25616-25618  is_revenue_platform
  5318-5326   list_archive_rules
  6343-6381   live
  8632-8640   live_check_worker
  3572-3593   llm_chat
  3642-3698   llm_chat_stream_sync
  3627-3639   llm_chat_sync
  3612-3624   llm_list_models
  4855-4881   log_event
  1340-1373   log_recording_failure
  8212-8261   logs_cmd
 32439-32829  main
  7065-7088   on_ai_media
  8338-8364   on_ai_reply
  8367-8396   on_azrael_mention
  8428-8458   on_callback
 22616-22710  oracle_handle
  8101-8104   pause_tracking
  6203-6208   profile_keyboard
  5857-5893   quick_restart_tracking
  8163-8209   quota
  8991-9054   reaper_loop
  5442-5444   record_tiktok_status
  7104-7134   recstatus
  3522-3530   redis_get_json
  3532-3538   redis_set_json
  4549-4573   remove_tracking
  4919-4930   remove_tracking_tag
  4086-4221   rename_archive_entry
 31967-31977  report_cmd
 13041-13043  report_proxy_result
  2231-2258   resolve_tiktok_live_stream
  5708-5723   restore_recording
  8107-8110   resume_tracking
  5356-5436   run_archive_rules
 31980-32161  run_bot
 16183-16230  run_flask
  5234-5279   sample_bandwidth_for_active
  5285-5304   save_profile_snapshot
  4378-4384   save_tiktok_check
  4780-4786   set_recording_file
  4592-4630   set_tracking_paused
  4955-4984   set_tracking_priority
  5692-5706   soft_delete_recording
  9303-9916   split_and_send_video
  6256-6298   start
  4270-4284   start_recording_attempt
  7338-7376   stats
  5660-5677   stop_manual_recording
  8113-8160   stoprec
  5100-5116   store_inspect
  7563-7571   summary_cmd
  8264-8335   sysres
  6688-6832   teststream
  6300-6341   tiktok
  7958-8015   topusers
  6418-6475   track
  6383-6415   track_exact
  6489-6537   tracklist
  5526-5658   trigger_manual_recording
  4741-4778   try_acquire_recording_lock
  5737-5796   universal_search
  6477-6487   untrack
  5122-5136   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
archive.py             compute_recording_fingerprint, evaluate_archive_rule, get_archive_entries_paged, run_archive_file_check
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
channels.py            configure_chat
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
cookies.py             —
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur
evolution.py           analyze
ffdiag.py              redact_cmd_for_log
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           class MarketingConfig, class MarketingState, compose, has_content, next_due_ts, should_post, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, stateless_reason, twitch_roles
news.py                build_items, class NewsConfig, class NewsState, item_id, merge, render_json, should_generate
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy
recdiag.py             disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_targets.py    all_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap
story.py               class StoryMemory, configure
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
