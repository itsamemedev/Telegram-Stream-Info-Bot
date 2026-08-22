# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (345)

```
 10963  GET              /                                                dashboard
 17246  GET              /api/abo/status                                  api_abo_status
 11062  GET              /api/active-recordings                           api_active_recordings
 17321  GET              /api/activity-pulse                              api_activity_pulse
 16199  GET              /api/ai-log                                      api_ai_log
 11460  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 26973  GET              /api/ai/anomalies                                api_ai_anomalies
 13194  POST             /api/ai/ask                                      api_ai_ask
 14429  POST             /api/ai/claude/save                              api_claude_save
 14409  GET              /api/ai/claude/status                            api_claude_status
 14447  POST             /api/ai/claude/test                              api_claude_test
 13457  GET              /api/ai/config                                   api_ai_config
 11632  GET              /api/ai/conversations                            api_ai_conversations_list
 11643  POST             /api/ai/conversations                            api_ai_conversations_create
 11653  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get
 11676  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete
 11683  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch
 11694  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send
 11827  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream
 12496  POST             /api/ai/diagnose                                 api_ai_diagnose
 27211  GET              /api/ai/forecast-storage                         api_ai_forecast_storage
 27245  GET              /api/ai/health-score/<username>                  api_ai_health_score
 11616  GET              /api/ai/models                                   api_ai_models
 26926  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive
 26906  POST             /api/ai/query                                    api_ai_query
 27079  GET              /api/ai/recommendations                          api_ai_recommendations
 27127  GET              /api/ai/report                                   api_ai_report
 27178  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice
 27037  GET              /api/ai/segments                                 api_ai_segments
 26881  GET              /api/ai/skills                                   api_ai_skills
 17048  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 16244  GET              /api/archive                                     api_archive
 16540  DELETE           /api/archive/<int:eid>                           api_archive_delete
 16399  POST             /api/archive/<int:eid>/rename                    api_archive_rename
 16377  POST             /api/archive/bulk-delete                         api_archive_bulk_delete
 16367  GET              /api/archive/check                               api_archive_check
 12603  GET              /api/archive/duplicates                          api_archive_duplicates
 12619  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete
 25054  POST             /api/archive/index/<int:rid>                     api_archive_index_one
 25019  GET              /api/archive/search                              api_archive_search
 25039  GET              /api/archive/status                              api_archive_status
 16432  POST             /api/archive/upload                              api_archive_upload
 25299  GET/POST         /api/audio/config                                api_audio_config
 25329  POST             /api/audio/testtone                              api_audio_testtone
 17154  GET/POST         /api/auto-archive-rules                          api_archive_rules
 17178  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 17182  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 13407  GET              /api/automation/status                           api_automation_status
 13429  POST             /api/automation/toggle                           api_automation_toggle
 15231  GET              /api/azrael/agents                               api_azrael_agents
 13313  POST             /api/azrael/ask                                  api_azrael_ask
 25535  GET/POST         /api/azrael/context                              api_azrael_context
 14869  GET              /api/azrael/core                                 api_azrael_core
 25669  POST             /api/azrael/live_pause                           api_azrael_live_pause
 25659  GET              /api/azrael/live_status                          api_azrael_live_status
 25677  POST             /api/azrael/live_test                            api_azrael_live_test
 15240  GET              /api/azrael/memories                             api_azrael_memories
 25725  POST             /api/azrael/persona                              api_azrael_persona_set
 25716  GET              /api/azrael/personas                             api_azrael_personas
 25753  GET              /api/azrael/piper_status                         api_azrael_piper_status
 25508  POST             /api/azrael/react                                api_azrael_react
 25544  GET              /api/azrael/reaction                             api_azrael_reaction
 25696  GET              /api/azrael/reactions                            api_azrael_reactions
 25746  GET              /api/azrael/transcript                           api_azrael_transcript
 25631  POST             /api/azrael/tts_test                             api_azrael_tts_test
 25606  GET              /api/azrael/voices                               api_azrael_voices
 25770  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 12014  GET              /api/backoff-watch                               api_backoff_watch
 15855  POST             /api/backup/run                                  api_backup_run
 15821  GET              /api/backup/status                               api_backup_status
 15810  POST             /api/backup/system                               api_backup_system
 17120  GET              /api/bandwidth/live                              api_bandwidth_live
 17015  GET              /api/bookmarks                                   api_bookmarks_list
 12277  GET              /api/brain                                       api_brain
 12214  GET              /api/brain/alarms                                api_brain_alarms
 12199  GET              /api/brain/creator                               api_brain_creator
 12176  GET              /api/brain/graph                                 api_brain_graph
 12237  GET              /api/brain/growth                                api_brain_growth
 10559  GET              /api/brain/health                                api_brain_health
 26251  GET              /api/channel/categories                          api_channel_categories
 26257  POST             /api/channel/set                                 api_channel_set
 26067  GET              /api/channels/status                             api_channels_status
 24869  POST             /api/chat/send                                   api_chat_send
 15542  GET              /api/chat/send_status                            api_chat_send_status
 11043  GET              /api/checks                                      api_checks
 25572  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 25555  GET              /api/clips                                       api_clips
 25588  POST/DELETE      /api/clips/clear                                 api_clips_clear
 25174  GET              /api/cohost                                      api_cohost
 25186  POST             /api/cohost/config                               api_cohost_config
 18028  GET/POST         /api/collections                                 api_collections
 18063  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify
 18127  GET              /api/collections/<int:cid>/trackings             api_collection_trackings
 18468  GET              /api/community/stats                             api_community_stats
 27751  POST             /api/config/restore                              api_config_restore
 27736  GET              /api/config/snapshot                             api_config_snapshot
 17389  GET              /api/cookies/age                                 api_cookies_age
 11110  GET              /api/cookies/health                              api_cookies_health
 11117  POST             /api/cookies/update                              api_cookies_update
 27702  GET              /api/data/export                                 api_data_export
 18998  GET              /api/db/export                                   api_db_export
 19025  POST             /api/db/import                                   api_db_import
 18985  GET              /api/db/summary                                  api_db_summary
 25100  GET              /api/debug/threads                               api_debug_threads
 28637  GET              /api/defense/attacks                             api_defense_attacks
 28604  GET              /api/defense/crowdsec                            api_defense_crowdsec
 28622  GET              /api/defense/fail2ban                            api_defense_fail2ban
 28328  GET              /api/defense/overview                            api_defense_overview
 15917  POST             /api/discord/announce                            api_discord_announce
 15645  GET              /api/discord/clips_week                          api_discord_clips_week
 15861  GET              /api/discord/community                           api_discord_community
 15570  GET              /api/discord/invite                              api_discord_invite
 14989  GET              /api/discord/overview                            api_discord_overview
 15075  POST             /api/discord/webhook_test                        api_discord_webhook_test
 18545  POST             /api/donations/add                               api_donations_add
 18578  GET              /api/donations/manual                            api_donations_manual
 18586  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 18481  POST             /api/donations/reset                             api_donations_reset
 18602  GET              /api/donations/summary                           api_donations_summary
 17102  GET              /api/events                                      api_events
 15692  GET              /api/events/stream                               api_events_stream
 19653  GET              /api/evolution/changelog                         api_evolution_changelog
 19638  GET              /api/evolution/history                           api_evolution_history
 19578  GET              /api/evolution/learned                           api_evolution_learned
 19600  GET              /api/evolution/proposals                         api_evolution_proposals
 19621  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 19568  POST             /api/evolution/run                               api_evolution_run
 19668  GET              /api/evolution/snapshots                         api_evolution_snapshots
 19533  GET              /api/evolution/status                            api_evolution_status
 18812  GET              /api/finanzamt/entries                           api_finanzamt_entries
 18832  POST             /api/finanzamt/entry                             api_finanzamt_add
 18859  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 17115  GET              /api/forecast/storage                            api_forecast_storage
 13445  GET              /api/freeai/status                               api_freeai_status
 14942  GET              /api/health                                      api_health
 11932  GET              /api/health-score                                api_health_score
 17133  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 17129  GET              /api/heatmap/recordings                          api_heatmap_recordings
 25223  GET              /api/highlights                                  api_highlights
 25235  POST             /api/highlights/config                           api_highlights_config
 17833  GET              /api/insights/activity-clock                     api_insights_activity_clock
 17708  GET              /api/insights/best-times/<username>              api_insights_best_times
 17815  GET              /api/insights/catch-rate                         api_insights_catch_rate
 17790  GET              /api/insights/growth/<username>                  api_insights_growth
 17854  GET              /api/insights/leaderboard                        api_insights_leaderboard
 17741  GET              /api/insights/reliability                        api_insights_reliability
 17764  GET              /api/insights/session-stats                      api_insights_session_stats
 17888  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer
 26108  GET              /api/kick/channel                                api_kick_channel
 26129  POST             /api/kick/channel                                api_kick_channel_set
 14669  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 14737  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 14715  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 14654  GET              /api/kick/oauth/start                            api_kick_oauth_start
 14694  GET              /api/kick/oauth/status                           api_kick_oauth_status
 25347  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 25416  POST             /api/kickmod/config                              api_kickmod_config
 25461  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 25475  GET              /api/kickmod/learned                             api_kickmod_learned
 25502  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 25482  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 25813  POST             /api/kickmod/say                                 api_kickmod_say
 25789  POST             /api/kickmod/start                               api_kickmod_start
 25387  GET              /api/kickmod/status                              api_kickmod_status
 25800  POST             /api/kickmod/stop                                api_kickmod_stop
 10895  POST             /api/login                                       dashboard_login_submit
 18453  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13896  POST             /api/marketing/config                            api_marketing_config
 13921  GET              /api/marketing/preview                           api_marketing_preview
 13931  POST             /api/marketing/send-now                          api_marketing_send_now
 13870  GET              /api/marketing/status                            api_marketing_status
 13888  POST             /api/marketing/toggle                            api_marketing_toggle
 25250  GET              /api/moderation/feed                             api_moderation_feed
 14500  POST             /api/news/config                                 api_news_config
 14466  GET              /api/news/creators                               api_news_creators
 14477  POST             /api/news/creators/generate                      api_news_creators_generate
 14542  POST             /api/news/generate-now                           api_news_generate_now
 14537  GET              /api/news/items                                  api_news_items
 14528  GET              /api/news/preview                                api_news_preview
 14396  GET              /api/news/status                                 api_news_status
 14492  POST             /api/news/toggle                                 api_news_toggle
 18310  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 15463  GET              /api/notify/status                               api_notify_status
 15474  POST             /api/notify/test                                 api_notify_test
 15449  GET              /api/ops/audit                                   api_ops_audit
 18381  GET              /api/ops/db-stats                                api_ops_db_stats
 18409  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 15255  GET              /api/ops/errors                                  api_ops_errors
 18330  GET              /api/ops/healthcheck                             api_ops_healthcheck
 19080  GET              /api/ops/log-tail                                api_ops_log_tail
 13293  GET              /api/ops/logtail                                 api_ops_logtail
 15196  GET              /api/ops/metrics                                 api_ops_metrics
 15179  GET              /api/ops/resource_history                        api_ops_resource_history
 19054  GET              /api/ops/version                                 api_ops_version
 11313  GET              /api/outcomes                                    api_outcomes
 26732  POST             /api/overlay/config                              api_overlay_config
 26719  POST             /api/overlay/event                               api_overlay_event
 26624  GET              /api/overlay/state                               api_overlay_state
 11346  GET              /api/profile/<username>                          api_profile
 17397  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 17141  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 17300  GET              /api/proxy/heatmap                               api_proxy_heatmap
 17277  GET              /api/proxy/trend                                 api_proxy_trend
 14370  GET              /api/public/stats                                api_public_stats
 10997  GET              /api/pulse                                       api_pulse
 27273  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify
 27357  GET              /api/rec/compress-candidates                     api_rec_compress_candidates
 27416  GET              /api/rec/orphans                                 api_rec_orphans
 27427  POST             /api/rec/orphans/clean                           api_rec_orphans_clean
 27260  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality
 27324  POST             /api/rec/retention/apply                         api_rec_retention_apply
 27311  POST             /api/rec/retention/preview                       api_rec_retention_preview
 27290  GET              /api/rec/timeline/<username>                     api_rec_timeline
 16223  GET              /api/recording-attempts                          api_recording_attempts
 17032  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations
 17027  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark
 17229  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint
 16947  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect
 17976  POST             /api/recordings/<int:rid>/label                  api_recording_label
 17191  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest
 17000  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes
 16973  GET              /api/recordings/<int:rid>/quality                api_recording_quality
 17950  POST             /api/recordings/<int:rid>/rating                 api_recording_rating
 17365  POST             /api/recordings/<int:rid>/restore                api_recording_restore
 17909  POST             /api/recordings/<int:rid>/star                   api_recording_star
 17361  POST             /api/recordings/<int:rid>/trash                  api_recording_trash
 17199  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform
 16065  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop
 17993  GET              /api/recordings/by-label/<label>                 api_recordings_by_label
 16152  GET              /api/recordings/daily                            api_recordings_daily
 17499  POST             /api/recordings/dedup-scan                       api_dedup_scan
 18963  GET              /api/recordings/disconnects                      api_recording_disconnects
 18011  GET              /api/recordings/labels                           api_recordings_labels
 16109  GET              /api/recordings/list                             api_recordings_list
 17356  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop
 17343  GET              /api/recordings/manual/list                      api_manual_list
 17327  POST             /api/recordings/manual/start                     api_manual_start
 17464  GET              /api/recordings/overview                         api_recordings_overview
 17929  GET              /api/recordings/starred                          api_recordings_starred
 17369  GET              /api/recordings/trash                            api_trash_list
 24804  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 24782  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 24823  POST             /api/restream/<int:rid>/start                    api_restream_start
 25121  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 26586  GET              /api/restream/chatfeed                           api_restream_chatfeed
 24758  POST             /api/restream/create                             api_restream_create
 14745  GET              /api/restream/deck                               api_restream_deck
 13381  GET              /api/restream/health                             api_restream_health
 26608  POST             /api/restream/layout                             api_restream_layout
 24731  GET              /api/restream/list                               api_restream_list
 13357  POST             /api/restream/report                             api_restream_report
 25134  POST             /api/restream/start_all                          api_restream_start_all
 25160  POST             /api/restream/stop_all                           api_restream_stop_all
 13644  GET              /api/restream/testpush                           api_testpush_status
 13669  POST             /api/restream/testpush                           api_testpush_run
 18718  GET              /api/restream/verify                             api_restream_verify
 15623  GET              /api/retention/preview                           api_retention_preview
 15632  POST             /api/retention/run                               api_retention_run
 27817  POST             /api/schedule/add                                api_schedule_add
 27807  GET              /api/schedule/list                               api_schedule_list
 27842  POST             /api/schedule/remove                             api_schedule_remove
 15505  POST             /api/scheduler/add                               api_scheduler_add
 15526  POST             /api/scheduler/delete                            api_scheduler_delete
 15492  GET              /api/scheduler/list                              api_scheduler_list
 15580  POST             /api/scheduler/toggle                            api_scheduler_toggle
 16937  GET              /api/search                                      api_search
 28375  GET              /api/selftest                                    api_selftest
 24840  GET              /api/shield/stats                                api_shield_stats
 11016  GET              /api/stats                                       api_stats
 17315  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 17242  GET              /api/stats/tiktok-status                         api_tiktok_status
 27782  GET              /api/stats/timeline                              api_stats_timeline
 11084  GET              /api/storage                                     api_storage
 11091  POST             /api/storage/cleanup                             api_storage_cleanup
 17217  GET              /api/stream/inspect/<username>                   api_stream_inspect
 13334  GET              /api/stream/timeline                             api_stream_timeline
 15063  GET              /api/stream/transcript                           api_stream_transcript
 27450  GET              /api/streamer/compare                            api_streamer_compare
 27649  POST             /api/streamer/delete/<username>                  api_streamer_delete
 15597  GET              /api/streamer/detail                             api_streamer_detail
 27674  GET              /api/streamer/digest/<username>                  api_streamer_digest
 27554  GET              /api/streamer/dormant                            api_streamer_dormant
 27630  GET              /api/streamer/exists/<username>                  api_streamer_exists
 27509  GET              /api/streamer/journal/<username>                 api_streamer_journal
 27474  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 27534  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14909  GET              /api/streamers/wall                              api_streamers_wall
 11233  GET              /api/summary/preview                             api_summary_preview
 16652  GET              /api/system                                      api_system
 16548  GET              /api/system-resources                            api_system_resources
 18666  GET              /api/system/check_timing                         api_check_timing
 18946  GET              /api/system/config_drift                         api_config_drift
 15099  GET              /api/system/config_snapshot                      api_system_config_snapshot
 15310  GET              /api/system/preflight                            api_system_preflight
 15436  GET              /api/system/preflight_history                    api_system_preflight_history
 15757  GET              /api/system/resilience                           api_system_resilience
 17053  GET              /api/tags                                        api_tags_list
 11057  GET              /api/top                                         api_top
 13267  GET              /api/trackings                                   api_trackings
 18098  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 18149  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 17089  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 17380  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 18178  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 17075  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15947  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15994  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 16023  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 16005  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 11250  POST             /api/trackings/bulk                              api_trackings_bulk
 15962  GET              /api/trackings/export                            api_trackings_export
 17057  GET              /api/trackings/tags-map                          api_trackings_tags_map
 17435  GET              /api/trackings/watchlist-export                  api_watchlist_export
 12069  GET              /api/trend-7d                                    api_trend_7d
 25620  GET              /api/tts/<fn>                                    api_tts_file
 13524  POST             /api/tunnel/set                                  api_tunnel_set
 13503  GET              /api/tunnel/status                               api_tunnel_status
 13535  POST             /api/tunnel/test                                 api_tunnel_test
 13516  POST             /api/tunnel/toggle                               api_tunnel_toggle
 18918  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 18895  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 18877  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 26760  GET              /api/upload_window                               api_upload_window
 11327  GET              /api/userstats                                   api_userstats
 14553  GET              /api/version                                     api_version
 18217  GET/POST         /api/webhooks                                    api_webhooks
 18257  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete
 18288  POST             /api/webhooks/<int:wid>/test                     api_webhook_test
 18272  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle
 18774  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 18795  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 18759  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 18743  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 32055  GET              /api/youtube/sendrate                            api_youtube_sendrate
 16515  GET              /archive/<int:eid>/download                      archive_download
 16682  GET              /download/<int:recording_id>                     download
 16184  GET              /health                                          health
 25069  GET              /healthz                                         healthz
 10884  GET              /login                                           dashboard_login_page
 10918  GET              /logout                                          dashboard_logout
 10925  GET              /manifest.webmanifest                            pwa_manifest
 15127  GET              /metrics                                         api_prometheus_metrics
 26569  GET              /overlay                                         overlay_page
 10949  GET              /pwa-icon-<variant>.png                          pwa_icon
 10935  GET              /sw.js                                           pwa_service_worker
```

## Discord-Slash-Commands (45)

```
 29080  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 29539  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 29171  /assign_role            Rolle/Gruppe einem Mitglied geben
 29217  /ban                    Mitglied bannen
 29871  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 29795  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 29835  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 29820  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 29662  /clips                  Letzte Highlight-Clips eines Users
 29132  /create_category        Kategorie anlegen
 29101  /create_channel         Text-Channel anlegen (optional in Kategorie)
 29160  /create_group           Nutzergruppe (= Rolle) anlegen
 29143  /create_role            Rolle / Nutzergruppe anlegen
 29117  /create_voice           Voice-Channel anlegen
 29453  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 29569  /event                  Community-Event ankündigen (Admin) — mit Countdown
 29612  /events                 Kommende Community-Events anzeigen
 29708  /follow                 Bei Live-Gang eines Streamers gepingt werden
 29692  /help                   Alle Bot-Befehle anzeigen
 29206  /kick                   Mitglied kicken
 29435  /leaderboard            Top-10 der Community nach XP
 29648  /livenow                Welche getrackten User sind gerade live
 29678  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 29509  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 29241  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 29421  /rank                   Dein Level und Rang anzeigen
 29635  /recstatus              Aktuell laufende Aufnahmen
 29182  /remove_role            Rolle/Gruppe entfernen
 29094  /restream_status        Restream-Status
 29193  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 29386  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 29404  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 29734  /stats                  Statistik zu einem getrackten Streamer
 29006  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 30030  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 29927  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 29903  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 29228  /timeout                Mitglied stummschalten (Minuten)
 29806  /topstreamers           Rangliste der Streamer nach Aufnahmen
 29036  /track                  TikTok-User tracken
 29020  /tracklist              Getrackte TikTok-User dieses Servers
 29723  /unfollow               Live-Pings für einen Streamer abbestellen
 29069  /untrack                TikTok-User nicht mehr tracken
 29756  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 29780  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 30514  on_member_join
 30476  on_message
 30117  on_raw_reaction_add
 30549  on_ready
```

## Top-Level-Symbole in bot_v37.py (573 Funktionen, 2 Klassen)

```
  2368-2369   _abo_key
  2389-2407   _abo_probe_dump
 27917-27927  _active_recorder_sync
 22044-22051  _ad_allowlist
 23157-23163  _agent_for
 27929-27947  _ai_calls_total_sync
 13180-13190  _ai_dashboard_rate_check
 23166-23182  _ai_telemetry
 23664-23682  _alert
 30662-30712  _alert_monitor_loop
 31086-31148  _announce_loop
  3310-3319   _anthropic_key
  3339-3351   _anthropic_model
  3322-3333   _anthropic_model_raw
  3954-3964   _archive_open_unique
 10687-10690  _arg_int
  2360-2365   _as_dict
 20250-20255  _audio_cfg
 23818-23840  _audio_tap_cmd
 10820-10831  _auth_cookie
 10787-10816  _auth_guard
  1516-1521   _auto_on
 24707-24725  _auto_restream_loop
 32216-32231  _azrael_broadcast_reply
 32116-32138  _azrael_chat_reply
 32099-32113  _azrael_chat_should_reply
 14096-14114  _azrael_creator_take
 32144-32146  _azrael_gate_cfg
 23187-23201  _azrael_live_state
 26468-26482  _azrael_overlay_state
 23547-23601  _azrael_proactive_loop
 23006-23062  _azrael_reaction_to_chats
 32149-32156  _azrael_reply_all_chats
 32086-32096  _azrael_self_names
 32184-32213  _azrael_send_to
 23204-23225  _azrael_system
 30826-30829  _backup_active
 30907-30920  _backup_loop
 21932-21933  _badwords_path
 30627-30636  _brain_growth_loop
 12145-12172  _brain_growth_snapshot
  2296-2316   _brain_hint_delay
 12137-12139  _brain_history_for
  7291-7319   _brain_notify
 12114-12135  _brain_record
 12141-12143  _brain_stream_recent
 15671-15688  _browser_push
 11587-11607  _build_context_for_llm
  7335-7422   _build_daily_summary
  2799-2979   _build_native_cmd
 20598-20785  _build_restream_cmd
  3023-3056   _build_ytdlp_cmd
 27869-27876  _cached_probe
  6113-6140   _can_stop_tracking
  1696-1718   _capture_set_cookies
 17552-17564  _cfg_get
 17567-17574  _cfg_set
 26212-26247  _channel_set_all
 19848-19851  _chat_connected
 19854-19870  _chat_disconnected
  9284-9295   _chat_is_forum
 19890-19892  _chat_sanitize
 19894-19903  _chat_src_ok
 19833-19845  _chat_stat
 19873-19876  _chat_stats_snapshot
  3693-3704   _check_ai_alive_sync
  3707-3719   _check_ai_models_sync
 27878-27891  _check_redis_alive_sync
 27893-27913  _check_redis_version_sync
 12875-12918  _classify_pool_anonymity
 12921-12938  _classify_pool_anonymity_bg
   746-750    _claude_chat_sync_metered
 10712-10719  _client_ip
 31180-31207  _clip_prune
 31210-31220  _clip_recfile_for
 31736-31742  _clip_should_velocity
 31261-31343  _clip_to_discord
  3512-3521   _close_ai_session
 32260-32275  _cohost_broadcast
 32242-32246  _cohost_cfg
 32301-32313  _cohost_fire_highlight
 32249-32257  _cohost_gate
 32278-32298  _cohost_highlight
 31392-31426  _community_events_loop
 11530-11566  _conv_add_message
 11569-11574  _conv_archive
 11505-11514  _conv_create
 11519-11527  _conv_messages
 11577-11584  _conv_rename
  7715-7755   _cookie_alarm_loop
  1768-1772   _cookie_autorefresh_info
  1673-1677   _cookie_header
 15721-15753  _cpu_load_snapshot
  3901-3913   _create_index_safe
 14064-14079  _creator_activity
 14120-14143  _creator_dossier_generate
 14082-14093  _creator_facts_line
 28130-28236  _crowdsec_status
 28096-28127  _crowdsec_via_lapi
 27961-27979  _cscli_bin
 27985-27998  _cscli_path
  7608-7633   _daily_summary_loop
 28016-28033  _darf_journal_lesen
 30639-30659  _db_maintenance_loop
  7580-7605   _db_vacuum_loop
 22067-22091  _detect_foreign_ad
  1273-1284   _diag_path_owner
 23453-23497  _director_finalize
 24264-24271  _director_for
 23402-23450  _director_mark
 31630-31665  _disc_automod_check
 31603-31609  _disc_state_get
 31612-31619  _disc_state_set
 28679-28692  _discord_guild_filesize_bytes
 28878-28887  _discord_invite
 31564-31600  _discord_live_thread
 23604-23616  _discord_notify
 28779-28804  _discord_ops_alert
 31462-31560  _discord_post_user
 28943-30624  _discord_run_once
 28817-28875  _discord_start
 31151-31157  _discord_stop
 28700-28702  _discord_upload_limit_label
 28695-28697  _discord_upload_limit_mb
  7636-7710   _disk_alarm_loop
 33529-33578  _disk_autoclean
 33581-33594  _disk_guard_loop
 33521-33526  _disk_pct
 26525-26528  _donations_unknown_count
 20207-20209  _drawtext_chain
 16779-16781  _dump_all_threads
 12800-12864  _enrich_proxies_with_geo
  1913-1957   _ensure_cookie_file_netscape
 28890-28940  _ensure_discord_invite
 31357-31389  _ensure_error_channel
 13043-13080  _ensure_proxy_ready
  9297-9320   _ensure_topic
   626-628    _env_int
   631-633    _env_int_range
 31429-31459  _error_channel_loop
 23648-23661  _event_webhook
 19141-19147  _evo_build_dir
 19150-19157  _evo_version
 19433-19514  _evolution_cycle
 19166-19186  _evolution_llm_note
 19517-19527  _evolution_loop
 19189-19430  _evolution_write_build
  6733-6767   _extract_file_payload
  2045-2047   _extract_urls_from_streamurl_node
 28001-28008  _f2b_sudo_hint
 23684-23686  _faster_whisper_available
 21956-21968  _fetch_ldnoobw_de
 12689-12707  _fetch_proxy_list
 24098-24126  _fetch_tiktok_room_id
   677-680    _ff_cmd
 17689-17702  _ffmpeg_version_str
 20370-20375  _find_chromium
  3016-3020   _find_external_recorder
 27384-27412  _find_orphans
  2050-2052   _find_stream_urls
 17617-17642  _fire_webhooks
  8491-8500   _fork_safe
   761-770    _freeai_chat_sync_metered
 28051-28093  _geo_lookup_ips
  3501-3510   _get_ai_session
  8325-8365   _get_live_info
  2586-2593   _get_resolve_semaphore
  8646-9011   _handle_single_tracking
 33373-33375  _hb
 33378-33395  _hb_while
 19908-19910  _highlight_cfg
 19913-19942  _highlight_observe
 20378-20383  _htmlov_screenshot_cmd
 23842-23852  _httpx_proxy
 17650-17662  _in_quiet_hours
 34362-34393  _install_fast_eventloop
 10582-10636  _install_fast_json
 16784-16800  _install_faulthandler
 24950-24959  _intel_ensure_schema
 24984-25015  _intel_index_loop
 24971-24981  _intel_index_one
 24962-24968  _intel_semantic
  6102-6111   _is_authorized
  8576-8582   _is_dead
  2035-2037   _is_hevc
 28036-28042  _is_private_ip
  1419-1426   _is_process_running
  7321-7332   _is_quiet_hours
  1081-1090   _is_upload_window
 10671-10684  _json_error_handler
  7538-7568   _kick_broadcaster_id
 13570-13589  _kick_channel_live
  7455-7497   _kick_follower_count
 14632-14645  _kick_oauth_exchange
 14648-14650  _kick_oauth_page
 14591-14595  _kick_redirect_public
 14582-14588  _kick_redirect_source
 14568-14579  _kick_redirect_uri
  7440-7442   _kick_slug
 14598-14629  _kick_user_token
  3970-3978   _kind_from_filename
 17679-17684  _latest_popularity
 21978-21984  _learned_load
 21975-21976  _learned_path
 21986-21994  _learned_save
 24479-24509  _live_react_loop
 24275-24468  _live_react_worker
 23065-23076  _live_transcript_push
 24470-24477  _live_users
 23500-23544  _living_title_loop
  3564-3574   _llm_list_models
 21935-21943  _load_banned_words_file
  1594-1667   _load_cookies_dict
 30832-30904  _local_backup_scan
 10653-10667  _log_5xx
 20793-20797  _looks_like_codec_err
 20788-20790  _looks_like_source_expired
  8539-8569   _loop_fehler
 16804-16813  _loop_heartbeat
 33343-33370  _loop_lag_monitor
 16923-16926  _loop_not_ready
 16816-16884  _loop_watchdog_thread
 22945-22959  _loyalty_add
 22936-22942  _loyalty_get
 22962-22970  _loyalty_top
 18518-18536  _manual_donations_rows
 18539-18541  _manual_donations_total
  8584-8585   _mark_dead
 13737-13766  _marketing_cfg
 13728-13734  _marketing_default_targets
 13723-13725  _marketing_enabled
 13780-13795  _marketing_flavor
 13850-13866  _marketing_loop
 13798-13808  _marketing_post_discord
 13811-13823  _marketing_post_telegram
 13826-13847  _marketing_publish
 13769-13773  _marketing_state_obj
 13776-13777  _marketing_state_save
 32163-32181  _maybe_handle_command
 33680-33704  _maybe_hype_clip
  3868-3891   _migrate_columns
 32438-32449  _mod_is_exempt
 32452-32457  _mod_warn_first
 32460-32463  _mod_warn_text
 19696-19704  _modlog
   885-887    _multistream_targets
  8503-8504   _nc_create_subprocess_exec
  8507-8508   _nc_create_subprocess_shell
 13961-13977  _news_cfg
 13948-13950  _news_enabled
 14015-14056  _news_facts
 14170-14192  _news_generate
 14375-14392  _news_loop
 13953-13958  _news_output_path
 14059-14061  _news_phrase
 14146-14167  _news_phrase_impl
 13990-13997  _news_read
 13980-13983  _news_state_obj
 13986-13987  _news_state_save
 14000-14012  _news_write
 26853-26877  _nl_to_sql
 19734-19736  _normalize_ingest
  2227-2244   _note_check_duration
 23091-23099  _oracle_memories
 23357-23391  _oracle_memorize
 23102-23115  _oracle_persona
 23084-23088  _oracle_recent_text
 20033-20041  _ov_atomic_write
 20021-20027  _ov_bar
 21891-21903  _ov_clip_text
 20030-20031  _ov_oneline
 26536-26565  _overlay_push
 20324-20367  _overlay_render_size
 19795-19799  _overlay_session_reset
 26484-26487  _overlay_src_ok
 22054-22064  _own_invites
 18499-18515  _parse_eur
 20319-20321  _parse_size
 28244-28324  _parse_ssh_attacks
  7927-7960   _pause_resume_cmd
  1722-1766   _persist_refreshed_cookies
  1560-1592   _pick_checked_pull_proxy
 10739-10744  _pin_auth_value
 10776-10777  _pin_clear_fail
 10756-10759  _pin_locked
 10762-10773  _pin_note_fail
 10747-10753  _pin_ok
 26374-26376  _piper_available
 26339-26361  _piper_list_voices
 26381-26406  _piper_pick_model
 26418-26465  _piper_say
 26332-26336  _piper_voice_roots
 17579-17614  _post_json_threaded
 20298-20316  _probe_video_size
  1447-1464   _proc_is_recorder
 12787-12798  _proxy_geo_cache_put
 13014-13040  _proxy_pool_refresh_loop
  1526-1557   _proxy_report_recording
 16769-16771  _prune_stall_dumps
 14195-14316  _public_stats
 23619-23645  _push_notify
 10878-10880  _pwa_dir
 12758-12773  _quick_validate_proxy
 17645-17647  _quiet_hours_config
 10843-10876  _rate_guard
 22910-22916  _react_warn
  8411-8450   _reap_proc
  2267-2289   _record_check_outcome
   672-674    _redact_stream_urls
 12941-13011  _refresh_proxy_pool
 26364-26370  _resolve_piper_model
  2061-2151   _resolve_via_html
  2409-2563   _resolve_via_webcast_api_v2
  2626-2688   _resolve_via_ytdlp
 31782-31911  _resolve_youtube_ingest
 24548-24555  _restream_active_platforms
 19780-19791  _restream_active_sources
 24129-24228  _restream_chat_guardian
 19945-20017  _restream_chat_push
 19707-19719  _restream_enabled
 20386-20473  _restream_html_overlay_start
 20476-20489  _restream_html_overlay_stop
  1029-1031   _restream_layout_mode
 19745-19768  _restream_overlay_files
 24513-24545  _restream_platform_state
 24669-24704  _restream_resume_after_restart
 20537-20595  _restream_tts_enqueue_wav
 20260-20292  _restream_tts_feeder
 20257-20258  _restream_tts_fifo_path
 20492-20519  _restream_tts_start
 20521-20535  _restream_tts_stop
 24558-24666  _restream_verify_loop
 30797-30809  _retention_loop
 30756-30794  _retention_scan
  2371-2373   _room_is_abo
  6771-6888   _run_ai_call
 16907-16920  _run_async_from_flask
 28045-28048  _run_priv
 34350-34358  _run_selfcheck_and_exit
 30812-30823  _s3_client
 26817-26848  _safe_select
  8587-8633   _safe_send
  5139-5155   _sample_net_throughput
 21945-21953  _save_banned_words_file
  2319-2346   _schedule_next_check
 30715-30753  _scheduler_loop
  3894-3898   _schema_pk
 16928-16933  _scraper_session
 32466-32505  _screen_full
 14958-14984  _sec_headers
  2040-2042   _select_stream_from_data_section
 34163-34347  _selfcheck
  1104-1108   _should_defer_upload
 31223-31258  _shrink_for_discord
 33601-33618  _sign_health_check
 33621-33640  _sign_health_loop
  8520-8531   _spawn
 28368-28371  _st_befund
 23854-24095  _start_chat_listener
 16887-16904  _start_loop_watchdog
 14340-14366  _stats_loop
 14319-14322  _stats_output_path
 14325-14337  _stats_write
  9079-9093   _storage_cleanup_loop
 33660-33667  _story_for
  3078-3084   _stream_url_expiry
  3093-3099   _stream_url_is_fresh
  3086-3091   _stream_url_ttl
 22018-22025  _streamer_persona_get
 22000-22006  _streamer_personas_load
 21997-21998  _streamer_personas_path
 22008-22016  _streamer_personas_save
 20212-20216  _studio_chain
 30929-31051  _system_backup
 31054-31082  _system_backup_loop
 12710-12749  _test_proxy
 13611-13620  _testpush_cfg
 13623-13640  _testpush_exec
 13592-13608  _testpush_resolve_live
  9256-9266   _tg_topics_load_into_mem
  9253-9254   _tg_topics_path
  9268-9275   _tg_topics_save
 27578-27626  _tiktok_account_exists
 10722-10730  _token_ok
  9278-9282   _topic_forget
 17665-17676  _tracking_max_duration
  1331-1354   _try_attach_file_handler
 26408-26416  _tts_cleanup
 13496-13499  _tunnel_effective
 25834-25887  _twitch_channel_status
 32508-32650  _twitch_chat_loop
 32324-32425  _twitch_eventsub_loop
 18939-18942  _twitch_oauth_page
  1127-1140   _upload_queue_add
  1151-1153   _upload_queue_count
  1110-1119   _upload_queue_load
  1100-1102   _upload_queue_path
  1142-1149   _upload_queue_remove
  1121-1125   _upload_queue_save
  1155-1193   _upload_window_loop
  8384-8391   _uptime_s
 19722-19731  _url_host
   739-743    _usage_record_claude
  7500-7528   _viewer_sample_loop
  7570-7577   _viewer_stats
 10780-10783  _wants_html
  8394-8408   _warn_empty_env
 33416-33511  _watchdog_loop
 32065-32073  _wchat_thank_ok
 23688-23718  _whisper_get_model
  8481-8488   _whisper_native_section
 22897-22903  _whisper_pool
 23787-23816  _whisper_segments
 23720-23784  _whisper_transcribe
 20043-20205  _write_restream_overlay
 32678-32751  _youtube_api_chat_loop
 25890-25993  _youtube_api_status
 25996-26063  _youtube_channel_status
 32754-32911  _youtube_chat_loop
 31917-31930  _youtube_restream_autoconfig
 31933-31957  _youtube_restream_autoconfig_inner
 32023-32051  _youtube_send
 26168-26209  _youtube_set_channel
 31960-31994  _yt_access_token
 31997-32012  _yt_live_chat_id
 32671-32675  _yt_oauth_configured
 32018-32020  _yt_sendrate_cfg
 32653-32668  _yt_timeout
  2610-2611   _ytdlp_detect_available
  2613-2624   _ytdlp_note_result
 16774-16776  _zombie_child_count
  8261-8285   about
  4341-4360   add_ai_log_entry
  4229-4237   add_archive_entry
  5252-5267   add_archive_rule
  4785-4819   add_recording
  4446-4463   add_tracking
  4880-4897   add_tracking_tag
  6891-6924   ai
  3733-3772   ai_chat
  3806-3816   ai_history_append
  3818-3823   ai_history_clear
  3795-3804   ai_history_load
  3780-3793   ai_rate_limit_check
  6953-6961   aireset
  3943-3951   archive_writeable
 23228-23247  azrael_chat
 32916-33038  brain_cmd
  3102-3286   build_recording_cmd
  5687-5733   build_recording_manifest
  4466-4543   bulk_add_trackings
  4034-4074   bulk_delete_archive_entries
  7758-7817   bulkadd
  9096-9236   check_all_trackings
  4630-4642   claim_live_transition
 22094-22840  class KickModerator
 20800-21778  class RestreamManager
 13125-13167  classify_proxy_anonymity
  6999-7197   cleanup
  5962-6003   cleanup_old_recordings
  4776-4783   clear_recording
 31668-31733  clip_moment
  5400-5443   cluster_failures
  5083-5132   compute_storage_forecast
  5841-5908   compute_waveform_peaks
  7880-7924   cookies_cmd
  5736-5742   cookies_days_old
  4437-4443   count_trackings_for_chat
  4328-4339   decide_preferred_recorder
  4247-4271   delete_archive_entry
  5269-5277   delete_archive_rule
  6428-6575   diag
 33041-33102  einnahmen_cmd
  5012-5043   ffprobe_inspect
  5077-5080   find_recordings_by_fingerprint
  4289-4305   finish_recording_attempt
  4575-4585   get_all_active_trackings
  4382-4385   get_all_checks
  4821-4824   get_all_recordings
  4922-4932   get_all_tags_with_counts
  5005-5008   get_annotations_for_recording
  3989-4001   get_archive_aggregate_stats
  4239-4245   get_archive_entry
  4003-4015   get_archive_kind_breakdown
  4018-4032   get_archive_missing_ids
  4998-5001   get_bookmarked_recordings
  1789-1906   get_cookie_health
  4871-4877   get_event_log
  4312-4326   get_last_recording_attempt
  2691-2796   get_live_status
  5603-5606   get_manual_recordings
  5045-5048   get_or_compute_inspect_sync
  6038-6082   get_outcome_breakdown
  4979-4987   get_priority_poll_interval
  5230-5239   get_profile_snapshots
  4362-4372   get_recent_ai_log
  4307-4310   get_recent_recording_attempts
  4826-4829   get_recording_by_id
  4991-4994   get_recording_note
  3449-3472   get_redis
  4413-4429   get_stats
  5929-5960   get_storage_stats
  4912-4920   get_tags_for_tracking
  5370-5384   get_tiktok_status_distribution
  4966-4977   get_tracking_priority
  4644-4653   get_tracking_state
  4571-4573   get_trackings_for_group
  5619-5622   get_trash_recordings
  9940-10550  handle_recording_finished
  3916-3941   init_db
  5784-5838   inspect_stream_url
 26531-26533  is_revenue_platform
  5242-5250   list_archive_rules
  6232-6270   live
  8636-8644   live_check_worker
  3524-3558   llm_chat
  3623-3690   llm_chat_stream_sync
  3592-3620   llm_chat_sync
  3577-3589   llm_list_models
  4837-4863   log_event
  1381-1414   log_recording_failure
  8074-8123   logs_cmd
 33708-34153  main
  6927-6950   on_ai_media
  8200-8226   on_ai_reply
  8229-8258   on_azrael_mention
  8290-8320   on_callback
 23250-23354  oracle_handle
  7963-7966   pause_tracking
  6092-6097   profile_keyboard
  5745-5781   quick_restart_tracking
  8025-8071   quota
  9013-9076   reaper_loop
  5366-5368   record_tiktok_status
  6966-6996   recstatus
  3474-3482   redis_get_json
  3484-3490   redis_set_json
  4545-4569   remove_tracking
  4899-4910   remove_tracking_tag
  4089-4224   rename_archive_entry
 33105-33115  report_cmd
 13170-13172  report_proxy_result
  2154-2181   resolve_tiktok_live_stream
  5614-5617   restore_recording
  7969-7972   resume_tracking
  5280-5360   run_archive_rules
 33118-33323  run_bot
 16696-16743  run_flask
  5158-5203   sample_bandwidth_for_active
  5209-5228   save_profile_snapshot
  4374-4380   save_tiktok_check
  4768-4774   set_recording_file
  4588-4626   set_tracking_paused
  4935-4964   set_tracking_priority
  5609-5612   soft_delete_recording
  9325-9938   split_and_send_video
  6145-6187   start
  4273-4287   start_recording_attempt
  7200-7238   stats
  5584-5601   stop_manual_recording
  7975-8022   stoprec
  5050-5066   store_inspect
  7425-7433   summary_cmd
  8126-8197   sysres
  6577-6721   teststream
  6189-6230   tiktok
  7820-7877   topusers
  6307-6364   track
  6272-6304   track_exact
  6378-6426   tracklist
  5450-5582   trigger_manual_recording
  4729-4766   try_acquire_recording_lock
  5625-5684   universal_search
  6366-6376   untrack
  5072-5075   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
archive.py             compute_recording_fingerprint, evaluate_archive_rule, get_archive_entries_paged, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              build_payload, chat_sync, is_retired, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           class MarketingConfig, class MarketingState, compose, has_content, next_due_ts, should_post, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                build_items, class NewsConfig, class NewsState, item_id, merge, render_json, should_generate
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
trackingdb.py          claim_transition, get_state
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
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
