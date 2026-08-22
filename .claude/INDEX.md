# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (345)

```
 10996  GET              /                                                dashboard
 17293  GET              /api/abo/status                                  api_abo_status
 11095  GET              /api/active-recordings                           api_active_recordings
 17368  GET              /api/activity-pulse                              api_activity_pulse
 16246  GET              /api/ai-log                                      api_ai_log
 11493  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 27020  GET              /api/ai/anomalies                                api_ai_anomalies
 13227  POST             /api/ai/ask                                      api_ai_ask
 14465  POST             /api/ai/claude/save                              api_claude_save
 14445  GET              /api/ai/claude/status                            api_claude_status
 14483  POST             /api/ai/claude/test                              api_claude_test
 13493  GET              /api/ai/config                                   api_ai_config
 11665  GET              /api/ai/conversations                            api_ai_conversations_list
 11676  POST             /api/ai/conversations                            api_ai_conversations_create
 11686  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get
 11709  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete
 11716  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch
 11727  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send
 11860  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream
 12529  POST             /api/ai/diagnose                                 api_ai_diagnose
 27258  GET              /api/ai/forecast-storage                         api_ai_forecast_storage
 27292  GET              /api/ai/health-score/<username>                  api_ai_health_score
 11649  GET              /api/ai/models                                   api_ai_models
 26973  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive
 26953  POST             /api/ai/query                                    api_ai_query
 27126  GET              /api/ai/recommendations                          api_ai_recommendations
 27174  GET              /api/ai/report                                   api_ai_report
 27225  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice
 27084  GET              /api/ai/segments                                 api_ai_segments
 26928  GET              /api/ai/skills                                   api_ai_skills
 17095  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 16291  GET              /api/archive                                     api_archive
 16587  DELETE           /api/archive/<int:eid>                           api_archive_delete
 16446  POST             /api/archive/<int:eid>/rename                    api_archive_rename
 16424  POST             /api/archive/bulk-delete                         api_archive_bulk_delete
 16414  GET              /api/archive/check                               api_archive_check
 12636  GET              /api/archive/duplicates                          api_archive_duplicates
 12652  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete
 25101  POST             /api/archive/index/<int:rid>                     api_archive_index_one
 25066  GET              /api/archive/search                              api_archive_search
 25086  GET              /api/archive/status                              api_archive_status
 16479  POST             /api/archive/upload                              api_archive_upload
 25346  GET/POST         /api/audio/config                                api_audio_config
 25376  POST             /api/audio/testtone                              api_audio_testtone
 17201  GET/POST         /api/auto-archive-rules                          api_archive_rules
 17225  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 17229  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 13443  GET              /api/automation/status                           api_automation_status
 13465  POST             /api/automation/toggle                           api_automation_toggle
 15278  GET              /api/azrael/agents                               api_azrael_agents
 13346  POST             /api/azrael/ask                                  api_azrael_ask
 25582  GET/POST         /api/azrael/context                              api_azrael_context
 14905  GET              /api/azrael/core                                 api_azrael_core
 25716  POST             /api/azrael/live_pause                           api_azrael_live_pause
 25706  GET              /api/azrael/live_status                          api_azrael_live_status
 25724  POST             /api/azrael/live_test                            api_azrael_live_test
 15287  GET              /api/azrael/memories                             api_azrael_memories
 25772  POST             /api/azrael/persona                              api_azrael_persona_set
 25763  GET              /api/azrael/personas                             api_azrael_personas
 25800  GET              /api/azrael/piper_status                         api_azrael_piper_status
 25555  POST             /api/azrael/react                                api_azrael_react
 25591  GET              /api/azrael/reaction                             api_azrael_reaction
 25743  GET              /api/azrael/reactions                            api_azrael_reactions
 25793  GET              /api/azrael/transcript                           api_azrael_transcript
 25678  POST             /api/azrael/tts_test                             api_azrael_tts_test
 25653  GET              /api/azrael/voices                               api_azrael_voices
 25817  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 12047  GET              /api/backoff-watch                               api_backoff_watch
 15902  POST             /api/backup/run                                  api_backup_run
 15868  GET              /api/backup/status                               api_backup_status
 15857  POST             /api/backup/system                               api_backup_system
 17167  GET              /api/bandwidth/live                              api_bandwidth_live
 17062  GET              /api/bookmarks                                   api_bookmarks_list
 12310  GET              /api/brain                                       api_brain
 12247  GET              /api/brain/alarms                                api_brain_alarms
 12232  GET              /api/brain/creator                               api_brain_creator
 12209  GET              /api/brain/graph                                 api_brain_graph
 12270  GET              /api/brain/growth                                api_brain_growth
 10592  GET              /api/brain/health                                api_brain_health
 26298  GET              /api/channel/categories                          api_channel_categories
 26304  POST             /api/channel/set                                 api_channel_set
 26114  GET              /api/channels/status                             api_channels_status
 24916  POST             /api/chat/send                                   api_chat_send
 15589  GET              /api/chat/send_status                            api_chat_send_status
 11076  GET              /api/checks                                      api_checks
 25619  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 25602  GET              /api/clips                                       api_clips
 25635  POST/DELETE      /api/clips/clear                                 api_clips_clear
 25221  GET              /api/cohost                                      api_cohost
 25233  POST             /api/cohost/config                               api_cohost_config
 18075  GET/POST         /api/collections                                 api_collections
 18110  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify
 18174  GET              /api/collections/<int:cid>/trackings             api_collection_trackings
 18515  GET              /api/community/stats                             api_community_stats
 27798  POST             /api/config/restore                              api_config_restore
 27783  GET              /api/config/snapshot                             api_config_snapshot
 17436  GET              /api/cookies/age                                 api_cookies_age
 11143  GET              /api/cookies/health                              api_cookies_health
 11150  POST             /api/cookies/update                              api_cookies_update
 27749  GET              /api/data/export                                 api_data_export
 19045  GET              /api/db/export                                   api_db_export
 19072  POST             /api/db/import                                   api_db_import
 19032  GET              /api/db/summary                                  api_db_summary
 25147  GET              /api/debug/threads                               api_debug_threads
 28684  GET              /api/defense/attacks                             api_defense_attacks
 28651  GET              /api/defense/crowdsec                            api_defense_crowdsec
 28669  GET              /api/defense/fail2ban                            api_defense_fail2ban
 28375  GET              /api/defense/overview                            api_defense_overview
 15964  POST             /api/discord/announce                            api_discord_announce
 15692  GET              /api/discord/clips_week                          api_discord_clips_week
 15908  GET              /api/discord/community                           api_discord_community
 15617  GET              /api/discord/invite                              api_discord_invite
 15036  GET              /api/discord/overview                            api_discord_overview
 15122  POST             /api/discord/webhook_test                        api_discord_webhook_test
 18592  POST             /api/donations/add                               api_donations_add
 18625  GET              /api/donations/manual                            api_donations_manual
 18633  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 18528  POST             /api/donations/reset                             api_donations_reset
 18649  GET              /api/donations/summary                           api_donations_summary
 17149  GET              /api/events                                      api_events
 15739  GET              /api/events/stream                               api_events_stream
 19700  GET              /api/evolution/changelog                         api_evolution_changelog
 19685  GET              /api/evolution/history                           api_evolution_history
 19625  GET              /api/evolution/learned                           api_evolution_learned
 19647  GET              /api/evolution/proposals                         api_evolution_proposals
 19668  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 19615  POST             /api/evolution/run                               api_evolution_run
 19715  GET              /api/evolution/snapshots                         api_evolution_snapshots
 19580  GET              /api/evolution/status                            api_evolution_status
 18859  GET              /api/finanzamt/entries                           api_finanzamt_entries
 18879  POST             /api/finanzamt/entry                             api_finanzamt_add
 18906  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 17162  GET              /api/forecast/storage                            api_forecast_storage
 13481  GET              /api/freeai/status                               api_freeai_status
 14978  GET              /api/health                                      api_health
 11965  GET              /api/health-score                                api_health_score
 17180  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 17176  GET              /api/heatmap/recordings                          api_heatmap_recordings
 25270  GET              /api/highlights                                  api_highlights
 25282  POST             /api/highlights/config                           api_highlights_config
 17880  GET              /api/insights/activity-clock                     api_insights_activity_clock
 17755  GET              /api/insights/best-times/<username>              api_insights_best_times
 17862  GET              /api/insights/catch-rate                         api_insights_catch_rate
 17837  GET              /api/insights/growth/<username>                  api_insights_growth
 17901  GET              /api/insights/leaderboard                        api_insights_leaderboard
 17788  GET              /api/insights/reliability                        api_insights_reliability
 17811  GET              /api/insights/session-stats                      api_insights_session_stats
 17935  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer
 26155  GET              /api/kick/channel                                api_kick_channel
 26176  POST             /api/kick/channel                                api_kick_channel_set
 14705  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 14773  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 14751  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 14690  GET              /api/kick/oauth/start                            api_kick_oauth_start
 14730  GET              /api/kick/oauth/status                           api_kick_oauth_status
 25394  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 25463  POST             /api/kickmod/config                              api_kickmod_config
 25508  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 25522  GET              /api/kickmod/learned                             api_kickmod_learned
 25549  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 25529  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 25860  POST             /api/kickmod/say                                 api_kickmod_say
 25836  POST             /api/kickmod/start                               api_kickmod_start
 25434  GET              /api/kickmod/status                              api_kickmod_status
 25847  POST             /api/kickmod/stop                                api_kickmod_stop
 10928  POST             /api/login                                       dashboard_login_submit
 18500  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13932  POST             /api/marketing/config                            api_marketing_config
 13957  GET              /api/marketing/preview                           api_marketing_preview
 13967  POST             /api/marketing/send-now                          api_marketing_send_now
 13906  GET              /api/marketing/status                            api_marketing_status
 13924  POST             /api/marketing/toggle                            api_marketing_toggle
 25297  GET              /api/moderation/feed                             api_moderation_feed
 14536  POST             /api/news/config                                 api_news_config
 14502  GET              /api/news/creators                               api_news_creators
 14513  POST             /api/news/creators/generate                      api_news_creators_generate
 14578  POST             /api/news/generate-now                           api_news_generate_now
 14573  GET              /api/news/items                                  api_news_items
 14564  GET              /api/news/preview                                api_news_preview
 14432  GET              /api/news/status                                 api_news_status
 14528  POST             /api/news/toggle                                 api_news_toggle
 18357  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 15510  GET              /api/notify/status                               api_notify_status
 15521  POST             /api/notify/test                                 api_notify_test
 15496  GET              /api/ops/audit                                   api_ops_audit
 18428  GET              /api/ops/db-stats                                api_ops_db_stats
 18456  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 15302  GET              /api/ops/errors                                  api_ops_errors
 18377  GET              /api/ops/healthcheck                             api_ops_healthcheck
 19127  GET              /api/ops/log-tail                                api_ops_log_tail
 13326  GET              /api/ops/logtail                                 api_ops_logtail
 15243  GET              /api/ops/metrics                                 api_ops_metrics
 15226  GET              /api/ops/resource_history                        api_ops_resource_history
 19101  GET              /api/ops/version                                 api_ops_version
 11346  GET              /api/outcomes                                    api_outcomes
 26779  POST             /api/overlay/config                              api_overlay_config
 26766  POST             /api/overlay/event                               api_overlay_event
 26671  GET              /api/overlay/state                               api_overlay_state
 11379  GET              /api/profile/<username>                          api_profile
 17444  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 17188  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 17347  GET              /api/proxy/heatmap                               api_proxy_heatmap
 17324  GET              /api/proxy/trend                                 api_proxy_trend
 14406  GET              /api/public/stats                                api_public_stats
 11030  GET              /api/pulse                                       api_pulse
 27320  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify
 27404  GET              /api/rec/compress-candidates                     api_rec_compress_candidates
 27463  GET              /api/rec/orphans                                 api_rec_orphans
 27474  POST             /api/rec/orphans/clean                           api_rec_orphans_clean
 27307  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality
 27371  POST             /api/rec/retention/apply                         api_rec_retention_apply
 27358  POST             /api/rec/retention/preview                       api_rec_retention_preview
 27337  GET              /api/rec/timeline/<username>                     api_rec_timeline
 16270  GET              /api/recording-attempts                          api_recording_attempts
 17079  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations
 17074  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark
 17276  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint
 16994  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect
 18023  POST             /api/recordings/<int:rid>/label                  api_recording_label
 17238  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest
 17047  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes
 17020  GET              /api/recordings/<int:rid>/quality                api_recording_quality
 17997  POST             /api/recordings/<int:rid>/rating                 api_recording_rating
 17412  POST             /api/recordings/<int:rid>/restore                api_recording_restore
 17956  POST             /api/recordings/<int:rid>/star                   api_recording_star
 17408  POST             /api/recordings/<int:rid>/trash                  api_recording_trash
 17246  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform
 16112  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop
 18040  GET              /api/recordings/by-label/<label>                 api_recordings_by_label
 16199  GET              /api/recordings/daily                            api_recordings_daily
 17546  POST             /api/recordings/dedup-scan                       api_dedup_scan
 19010  GET              /api/recordings/disconnects                      api_recording_disconnects
 18058  GET              /api/recordings/labels                           api_recordings_labels
 16156  GET              /api/recordings/list                             api_recordings_list
 17403  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop
 17390  GET              /api/recordings/manual/list                      api_manual_list
 17374  POST             /api/recordings/manual/start                     api_manual_start
 17511  GET              /api/recordings/overview                         api_recordings_overview
 17976  GET              /api/recordings/starred                          api_recordings_starred
 17416  GET              /api/recordings/trash                            api_trash_list
 24851  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 24829  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 24870  POST             /api/restream/<int:rid>/start                    api_restream_start
 25168  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 26633  GET              /api/restream/chatfeed                           api_restream_chatfeed
 24805  POST             /api/restream/create                             api_restream_create
 14781  GET              /api/restream/deck                               api_restream_deck
 13417  GET              /api/restream/health                             api_restream_health
 26655  POST             /api/restream/layout                             api_restream_layout
 24778  GET              /api/restream/list                               api_restream_list
 13390  POST             /api/restream/report                             api_restream_report
 25181  POST             /api/restream/start_all                          api_restream_start_all
 25207  POST             /api/restream/stop_all                           api_restream_stop_all
 13680  GET              /api/restream/testpush                           api_testpush_status
 13705  POST             /api/restream/testpush                           api_testpush_run
 18765  GET              /api/restream/verify                             api_restream_verify
 15670  GET              /api/retention/preview                           api_retention_preview
 15679  POST             /api/retention/run                               api_retention_run
 27864  POST             /api/schedule/add                                api_schedule_add
 27854  GET              /api/schedule/list                               api_schedule_list
 27889  POST             /api/schedule/remove                             api_schedule_remove
 15552  POST             /api/scheduler/add                               api_scheduler_add
 15573  POST             /api/scheduler/delete                            api_scheduler_delete
 15539  GET              /api/scheduler/list                              api_scheduler_list
 15627  POST             /api/scheduler/toggle                            api_scheduler_toggle
 16984  GET              /api/search                                      api_search
 28422  GET              /api/selftest                                    api_selftest
 24887  GET              /api/shield/stats                                api_shield_stats
 11049  GET              /api/stats                                       api_stats
 17362  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 17289  GET              /api/stats/tiktok-status                         api_tiktok_status
 27829  GET              /api/stats/timeline                              api_stats_timeline
 11117  GET              /api/storage                                     api_storage
 11124  POST             /api/storage/cleanup                             api_storage_cleanup
 17264  GET              /api/stream/inspect/<username>                   api_stream_inspect
 13367  GET              /api/stream/timeline                             api_stream_timeline
 15110  GET              /api/stream/transcript                           api_stream_transcript
 27497  GET              /api/streamer/compare                            api_streamer_compare
 27696  POST             /api/streamer/delete/<username>                  api_streamer_delete
 15644  GET              /api/streamer/detail                             api_streamer_detail
 27721  GET              /api/streamer/digest/<username>                  api_streamer_digest
 27601  GET              /api/streamer/dormant                            api_streamer_dormant
 27677  GET              /api/streamer/exists/<username>                  api_streamer_exists
 27556  GET              /api/streamer/journal/<username>                 api_streamer_journal
 27521  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 27581  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14945  GET              /api/streamers/wall                              api_streamers_wall
 11266  GET              /api/summary/preview                             api_summary_preview
 16699  GET              /api/system                                      api_system
 16595  GET              /api/system-resources                            api_system_resources
 18713  GET              /api/system/check_timing                         api_check_timing
 18993  GET              /api/system/config_drift                         api_config_drift
 15146  GET              /api/system/config_snapshot                      api_system_config_snapshot
 15357  GET              /api/system/preflight                            api_system_preflight
 15483  GET              /api/system/preflight_history                    api_system_preflight_history
 15804  GET              /api/system/resilience                           api_system_resilience
 17100  GET              /api/tags                                        api_tags_list
 11090  GET              /api/top                                         api_top
 13300  GET              /api/trackings                                   api_trackings
 18145  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 18196  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 17136  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 17427  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 18225  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 17122  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15994  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 16041  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 16070  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 16052  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 11283  POST             /api/trackings/bulk                              api_trackings_bulk
 16009  GET              /api/trackings/export                            api_trackings_export
 17104  GET              /api/trackings/tags-map                          api_trackings_tags_map
 17482  GET              /api/trackings/watchlist-export                  api_watchlist_export
 12102  GET              /api/trend-7d                                    api_trend_7d
 25667  GET              /api/tts/<fn>                                    api_tts_file
 13560  POST             /api/tunnel/set                                  api_tunnel_set
 13539  GET              /api/tunnel/status                               api_tunnel_status
 13571  POST             /api/tunnel/test                                 api_tunnel_test
 13552  POST             /api/tunnel/toggle                               api_tunnel_toggle
 18965  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 18942  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 18924  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 26807  GET              /api/upload_window                               api_upload_window
 11360  GET              /api/userstats                                   api_userstats
 14589  GET              /api/version                                     api_version
 18264  GET/POST         /api/webhooks                                    api_webhooks
 18304  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete
 18335  POST             /api/webhooks/<int:wid>/test                     api_webhook_test
 18319  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle
 18821  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 18842  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 18806  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 18790  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 32102  GET              /api/youtube/sendrate                            api_youtube_sendrate
 16562  GET              /archive/<int:eid>/download                      archive_download
 16729  GET              /download/<int:recording_id>                     download
 16231  GET              /health                                          health
 25116  GET              /healthz                                         healthz
 10917  GET              /login                                           dashboard_login_page
 10951  GET              /logout                                          dashboard_logout
 10958  GET              /manifest.webmanifest                            pwa_manifest
 15174  GET              /metrics                                         api_prometheus_metrics
 26616  GET              /overlay                                         overlay_page
 10982  GET              /pwa-icon-<variant>.png                          pwa_icon
 10968  GET              /sw.js                                           pwa_service_worker
```

## Discord-Slash-Commands (45)

```
 29127  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 29586  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 29218  /assign_role            Rolle/Gruppe einem Mitglied geben
 29264  /ban                    Mitglied bannen
 29918  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 29842  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 29882  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 29867  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 29709  /clips                  Letzte Highlight-Clips eines Users
 29179  /create_category        Kategorie anlegen
 29148  /create_channel         Text-Channel anlegen (optional in Kategorie)
 29207  /create_group           Nutzergruppe (= Rolle) anlegen
 29190  /create_role            Rolle / Nutzergruppe anlegen
 29164  /create_voice           Voice-Channel anlegen
 29500  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 29616  /event                  Community-Event ankündigen (Admin) — mit Countdown
 29659  /events                 Kommende Community-Events anzeigen
 29755  /follow                 Bei Live-Gang eines Streamers gepingt werden
 29739  /help                   Alle Bot-Befehle anzeigen
 29253  /kick                   Mitglied kicken
 29482  /leaderboard            Top-10 der Community nach XP
 29695  /livenow                Welche getrackten User sind gerade live
 29725  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 29556  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 29288  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 29468  /rank                   Dein Level und Rang anzeigen
 29682  /recstatus              Aktuell laufende Aufnahmen
 29229  /remove_role            Rolle/Gruppe entfernen
 29141  /restream_status        Restream-Status
 29240  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 29433  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 29451  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 29781  /stats                  Statistik zu einem getrackten Streamer
 29053  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 30077  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 29974  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 29950  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 29275  /timeout                Mitglied stummschalten (Minuten)
 29853  /topstreamers           Rangliste der Streamer nach Aufnahmen
 29083  /track                  TikTok-User tracken
 29067  /tracklist              Getrackte TikTok-User dieses Servers
 29770  /unfollow               Live-Pings für einen Streamer abbestellen
 29116  /untrack                TikTok-User nicht mehr tracken
 29803  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 29827  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 30561  on_member_join
 30523  on_message
 30164  on_raw_reaction_add
 30596  on_ready
```

## Top-Level-Symbole in bot_v37.py (574 Funktionen, 2 Klassen)

```
  2368-2369   _abo_key
  2389-2407   _abo_probe_dump
 27964-27974  _active_recorder_sync
 22091-22098  _ad_allowlist
 23204-23210  _agent_for
 27976-27994  _ai_calls_total_sync
 13213-13223  _ai_dashboard_rate_check
 23213-23229  _ai_telemetry
 23711-23729  _alert
 30709-30759  _alert_monitor_loop
 31133-31195  _announce_loop
  3310-3319   _anthropic_key
  3339-3351   _anthropic_model
  3322-3333   _anthropic_model_raw
  3954-3964   _archive_open_unique
 10720-10723  _arg_int
  2360-2365   _as_dict
 20297-20302  _audio_cfg
 23865-23887  _audio_tap_cmd
 10853-10864  _auth_cookie
 10820-10849  _auth_guard
  1516-1521   _auto_on
 24754-24772  _auto_restream_loop
 32263-32278  _azrael_broadcast_reply
 32163-32185  _azrael_chat_reply
 32146-32160  _azrael_chat_should_reply
 14132-14150  _azrael_creator_take
 32191-32193  _azrael_gate_cfg
 23234-23248  _azrael_live_state
 26515-26529  _azrael_overlay_state
 23594-23648  _azrael_proactive_loop
 23053-23109  _azrael_reaction_to_chats
 32196-32203  _azrael_reply_all_chats
 32133-32143  _azrael_self_names
 32231-32260  _azrael_send_to
 23251-23272  _azrael_system
 30873-30876  _backup_active
 30954-30967  _backup_loop
 21979-21980  _badwords_path
 30674-30683  _brain_growth_loop
 12178-12205  _brain_growth_snapshot
  2296-2316   _brain_hint_delay
 12170-12172  _brain_history_for
  7291-7319   _brain_notify
 12147-12168  _brain_record
 12174-12176  _brain_stream_recent
 15718-15735  _browser_push
 11620-11640  _build_context_for_llm
  7335-7422   _build_daily_summary
  2799-2979   _build_native_cmd
 20645-20832  _build_restream_cmd
  3023-3056   _build_ytdlp_cmd
 27916-27923  _cached_probe
  6113-6140   _can_stop_tracking
  1696-1718   _capture_set_cookies
 17599-17611  _cfg_get
 17614-17621  _cfg_set
 26259-26294  _channel_set_all
 19895-19898  _chat_connected
 19901-19917  _chat_disconnected
  9317-9328   _chat_is_forum
 19937-19939  _chat_sanitize
 19941-19950  _chat_src_ok
 19880-19892  _chat_stat
 19920-19923  _chat_stats_snapshot
  3693-3704   _check_ai_alive_sync
  3707-3719   _check_ai_models_sync
 27925-27938  _check_redis_alive_sync
 27940-27960  _check_redis_version_sync
 12908-12951  _classify_pool_anonymity
 12954-12971  _classify_pool_anonymity_bg
   746-750    _claude_chat_sync_metered
 10745-10752  _client_ip
 31227-31254  _clip_prune
 31257-31267  _clip_recfile_for
 31783-31789  _clip_should_velocity
 31308-31390  _clip_to_discord
  3512-3521   _close_ai_session
 32307-32322  _cohost_broadcast
 32289-32293  _cohost_cfg
 32348-32360  _cohost_fire_highlight
 32296-32304  _cohost_gate
 32325-32345  _cohost_highlight
 31439-31473  _community_events_loop
 11563-11599  _conv_add_message
 11602-11607  _conv_archive
 11538-11547  _conv_create
 11552-11560  _conv_messages
 11610-11617  _conv_rename
  7715-7755   _cookie_alarm_loop
  1768-1772   _cookie_autorefresh_info
  1673-1677   _cookie_header
 15768-15800  _cpu_load_snapshot
  3901-3913   _create_index_safe
 14100-14115  _creator_activity
 14156-14179  _creator_dossier_generate
 14118-14129  _creator_facts_line
 28177-28283  _crowdsec_status
 28143-28174  _crowdsec_via_lapi
 28008-28026  _cscli_bin
 28032-28045  _cscli_path
  7608-7633   _daily_summary_loop
 28063-28080  _darf_journal_lesen
 30686-30706  _db_maintenance_loop
  7580-7605   _db_vacuum_loop
 22114-22138  _detect_foreign_ad
  1273-1284   _diag_path_owner
 23500-23544  _director_finalize
 24311-24318  _director_for
 23449-23497  _director_mark
 31677-31712  _disc_automod_check
 31650-31656  _disc_state_get
 31659-31666  _disc_state_set
 28726-28739  _discord_guild_filesize_bytes
 28925-28934  _discord_invite
 31611-31647  _discord_live_thread
 23651-23663  _discord_notify
 28826-28851  _discord_ops_alert
 31509-31607  _discord_post_user
 28990-30671  _discord_run_once
 28864-28922  _discord_start
 31198-31204  _discord_stop
 28747-28749  _discord_upload_limit_label
 28742-28744  _discord_upload_limit_mb
  7636-7710   _disk_alarm_loop
 33576-33625  _disk_autoclean
 33628-33641  _disk_guard_loop
 33568-33573  _disk_pct
 26572-26575  _donations_unknown_count
 20254-20256  _drawtext_chain
 16826-16828  _dump_all_threads
 12833-12897  _enrich_proxies_with_geo
  1913-1957   _ensure_cookie_file_netscape
 28937-28987  _ensure_discord_invite
 31404-31436  _ensure_error_channel
 13076-13113  _ensure_proxy_ready
  9330-9353   _ensure_topic
   626-628    _env_int
   631-633    _env_int_range
 31476-31506  _error_channel_loop
 23695-23708  _event_webhook
 19188-19194  _evo_build_dir
 19197-19204  _evo_version
 19480-19561  _evolution_cycle
 19213-19233  _evolution_llm_note
 19564-19574  _evolution_loop
 19236-19477  _evolution_write_build
  6733-6767   _extract_file_payload
  2045-2047   _extract_urls_from_streamurl_node
 28048-28055  _f2b_sudo_hint
 23731-23733  _faster_whisper_available
 22003-22015  _fetch_ldnoobw_de
 12722-12740  _fetch_proxy_list
 24145-24173  _fetch_tiktok_room_id
   677-680    _ff_cmd
 17736-17749  _ffmpeg_version_str
 20417-20422  _find_chromium
  3016-3020   _find_external_recorder
 27431-27459  _find_orphans
  2050-2052   _find_stream_urls
 17664-17689  _fire_webhooks
  8491-8500   _fork_safe
   761-770    _freeai_chat_sync_metered
 28098-28140  _geo_lookup_ips
  3501-3510   _get_ai_session
  8325-8365   _get_live_info
  2586-2593   _get_resolve_semaphore
  8679-9044   _handle_single_tracking
 33420-33422  _hb
 33425-33442  _hb_while
 19955-19957  _highlight_cfg
 19960-19989  _highlight_observe
 20425-20430  _htmlov_screenshot_cmd
 23889-23899  _httpx_proxy
 17697-17709  _in_quiet_hours
 34409-34440  _install_fast_eventloop
 10615-10669  _install_fast_json
 16831-16847  _install_faulthandler
 24997-25006  _intel_ensure_schema
 25031-25062  _intel_index_loop
 25018-25028  _intel_index_one
 25009-25015  _intel_semantic
  6102-6111   _is_authorized
  8609-8615   _is_dead
  2035-2037   _is_hevc
 28083-28089  _is_private_ip
  1419-1426   _is_process_running
  7321-7332   _is_quiet_hours
  1081-1090   _is_upload_window
 10704-10717  _json_error_handler
  7538-7568   _kick_broadcaster_id
 13606-13625  _kick_channel_live
  7455-7497   _kick_follower_count
 14668-14681  _kick_oauth_exchange
 14684-14686  _kick_oauth_page
 14627-14631  _kick_redirect_public
 14618-14624  _kick_redirect_source
 14604-14615  _kick_redirect_uri
  7440-7442   _kick_slug
 14634-14665  _kick_user_token
  3970-3978   _kind_from_filename
 17726-17731  _latest_popularity
 22025-22031  _learned_load
 22022-22023  _learned_path
 22033-22041  _learned_save
 24526-24556  _live_react_loop
 24322-24515  _live_react_worker
 23112-23123  _live_transcript_push
 24517-24524  _live_users
 23547-23591  _living_title_loop
  3564-3574   _llm_list_models
 21982-21990  _load_banned_words_file
  1594-1667   _load_cookies_dict
 30879-30951  _local_backup_scan
 10686-10700  _log_5xx
 20840-20844  _looks_like_codec_err
 20835-20837  _looks_like_source_expired
  8572-8602   _loop_fehler
 16851-16860  _loop_heartbeat
 33390-33417  _loop_lag_monitor
 16970-16973  _loop_not_ready
 16863-16931  _loop_watchdog_thread
 22992-23006  _loyalty_add
 22983-22989  _loyalty_get
 23009-23017  _loyalty_top
 18565-18583  _manual_donations_rows
 18586-18588  _manual_donations_total
  8617-8618   _mark_dead
 13773-13802  _marketing_cfg
 13764-13770  _marketing_default_targets
 13759-13761  _marketing_enabled
 13816-13831  _marketing_flavor
 13886-13902  _marketing_loop
 13834-13844  _marketing_post_discord
 13847-13859  _marketing_post_telegram
 13862-13883  _marketing_publish
 13805-13809  _marketing_state_obj
 13812-13813  _marketing_state_save
 32210-32228  _maybe_handle_command
 33727-33751  _maybe_hype_clip
  3868-3891   _migrate_columns
 32485-32496  _mod_is_exempt
 32499-32504  _mod_warn_first
 32507-32510  _mod_warn_text
 19743-19751  _modlog
   885-887    _multistream_targets
  8503-8504   _nc_create_subprocess_exec
  8507-8508   _nc_create_subprocess_shell
 13997-14013  _news_cfg
 13984-13986  _news_enabled
 14051-14092  _news_facts
 14206-14228  _news_generate
 14411-14428  _news_loop
 13989-13994  _news_output_path
 14095-14097  _news_phrase
 14182-14203  _news_phrase_impl
 14026-14033  _news_read
 14016-14019  _news_state_obj
 14022-14023  _news_state_save
 14036-14048  _news_write
 26900-26924  _nl_to_sql
 19781-19783  _normalize_ingest
  2227-2244   _note_check_duration
 23138-23146  _oracle_memories
 23404-23438  _oracle_memorize
 23149-23162  _oracle_persona
 23131-23135  _oracle_recent_text
 20080-20088  _ov_atomic_write
 20068-20074  _ov_bar
 21938-21950  _ov_clip_text
 20077-20078  _ov_oneline
 26583-26612  _overlay_push
 20371-20414  _overlay_render_size
 19842-19846  _overlay_session_reset
 26531-26534  _overlay_src_ok
 22101-22111  _own_invites
 18546-18562  _parse_eur
 20366-20368  _parse_size
 28291-28371  _parse_ssh_attacks
  7927-7960   _pause_resume_cmd
  1722-1766   _persist_refreshed_cookies
  1560-1592   _pick_checked_pull_proxy
 10772-10777  _pin_auth_value
 10809-10810  _pin_clear_fail
 10789-10792  _pin_locked
 10795-10806  _pin_note_fail
 10780-10786  _pin_ok
 26421-26423  _piper_available
 26386-26408  _piper_list_voices
 26428-26453  _piper_pick_model
 26465-26512  _piper_say
 26379-26383  _piper_voice_roots
 17626-17661  _post_json_threaded
 20345-20363  _probe_video_size
  1447-1464   _proc_is_recorder
 12820-12831  _proxy_geo_cache_put
 13047-13073  _proxy_pool_refresh_loop
  1526-1557   _proxy_report_recording
 16816-16818  _prune_stall_dumps
 14231-14352  _public_stats
 23666-23692  _push_notify
 10911-10913  _pwa_dir
 12791-12806  _quick_validate_proxy
 17692-17694  _quiet_hours_config
 10876-10909  _rate_guard
 22957-22963  _react_warn
  8411-8450   _reap_proc
  2267-2289   _record_check_outcome
   672-674    _redact_stream_urls
 12974-13044  _refresh_proxy_pool
 26411-26417  _resolve_piper_model
  2061-2151   _resolve_via_html
  2409-2563   _resolve_via_webcast_api_v2
  2626-2688   _resolve_via_ytdlp
 31829-31958  _resolve_youtube_ingest
 24595-24602  _restream_active_platforms
 19827-19838  _restream_active_sources
 24176-24275  _restream_chat_guardian
 19992-20064  _restream_chat_push
 19754-19766  _restream_enabled
 20433-20520  _restream_html_overlay_start
 20523-20536  _restream_html_overlay_stop
  1029-1031   _restream_layout_mode
 19792-19815  _restream_overlay_files
 24560-24592  _restream_platform_state
 24716-24751  _restream_resume_after_restart
 20584-20642  _restream_tts_enqueue_wav
 20307-20339  _restream_tts_feeder
 20304-20305  _restream_tts_fifo_path
 20539-20566  _restream_tts_start
 20568-20582  _restream_tts_stop
 24605-24713  _restream_verify_loop
 30844-30856  _retention_loop
 30803-30841  _retention_scan
  2371-2373   _room_is_abo
  6771-6888   _run_ai_call
 16954-16967  _run_async_from_flask
 28092-28095  _run_priv
 34397-34405  _run_selfcheck_and_exit
 30859-30870  _s3_client
 26864-26895  _safe_select
  8620-8666   _safe_send
  5139-5155   _sample_net_throughput
 21992-22000  _save_banned_words_file
  2319-2346   _schedule_next_check
 30762-30800  _scheduler_loop
  3894-3898   _schema_pk
 16975-16980  _scraper_session
 32513-32552  _screen_full
 14994-15031  _sec_headers
  2040-2042   _select_stream_from_data_section
 34210-34394  _selfcheck
  1104-1108   _should_defer_upload
 31270-31305  _shrink_for_discord
 33648-33665  _sign_health_check
 33668-33687  _sign_health_loop
  8520-8531   _spawn
  8534-8564   _spawn_from_flask
 28415-28418  _st_befund
 23901-24142  _start_chat_listener
 16934-16951  _start_loop_watchdog
 14376-14402  _stats_loop
 14355-14358  _stats_output_path
 14361-14373  _stats_write
  9112-9126   _storage_cleanup_loop
 33707-33714  _story_for
  3078-3084   _stream_url_expiry
  3093-3099   _stream_url_is_fresh
  3086-3091   _stream_url_ttl
 22065-22072  _streamer_persona_get
 22047-22053  _streamer_personas_load
 22044-22045  _streamer_personas_path
 22055-22063  _streamer_personas_save
 20259-20263  _studio_chain
 30976-31098  _system_backup
 31101-31129  _system_backup_loop
 12743-12782  _test_proxy
 13647-13656  _testpush_cfg
 13659-13676  _testpush_exec
 13628-13644  _testpush_resolve_live
  9289-9299   _tg_topics_load_into_mem
  9286-9287   _tg_topics_path
  9301-9308   _tg_topics_save
 27625-27673  _tiktok_account_exists
 10755-10763  _token_ok
  9311-9315   _topic_forget
 17712-17723  _tracking_max_duration
  1331-1354   _try_attach_file_handler
 26455-26463  _tts_cleanup
 13532-13535  _tunnel_effective
 25881-25934  _twitch_channel_status
 32555-32697  _twitch_chat_loop
 32371-32472  _twitch_eventsub_loop
 18986-18989  _twitch_oauth_page
  1127-1140   _upload_queue_add
  1151-1153   _upload_queue_count
  1110-1119   _upload_queue_load
  1100-1102   _upload_queue_path
  1142-1149   _upload_queue_remove
  1121-1125   _upload_queue_save
  1155-1193   _upload_window_loop
  8384-8391   _uptime_s
 19769-19778  _url_host
   739-743    _usage_record_claude
  7500-7528   _viewer_sample_loop
  7570-7577   _viewer_stats
 10813-10816  _wants_html
  8394-8408   _warn_empty_env
 33463-33558  _watchdog_loop
 32112-32120  _wchat_thank_ok
 23735-23765  _whisper_get_model
  8481-8488   _whisper_native_section
 22944-22950  _whisper_pool
 23834-23863  _whisper_segments
 23767-23831  _whisper_transcribe
 20090-20252  _write_restream_overlay
 32725-32798  _youtube_api_chat_loop
 25937-26040  _youtube_api_status
 26043-26110  _youtube_channel_status
 32801-32958  _youtube_chat_loop
 31964-31977  _youtube_restream_autoconfig
 31980-32004  _youtube_restream_autoconfig_inner
 32070-32098  _youtube_send
 26215-26256  _youtube_set_channel
 32007-32041  _yt_access_token
 32044-32059  _yt_live_chat_id
 32718-32722  _yt_oauth_configured
 32065-32067  _yt_sendrate_cfg
 32700-32715  _yt_timeout
  2610-2611   _ytdlp_detect_available
  2613-2624   _ytdlp_note_result
 16821-16823  _zombie_child_count
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
 23275-23294  azrael_chat
 32963-33085  brain_cmd
  3102-3286   build_recording_cmd
  5687-5733   build_recording_manifest
  4466-4543   bulk_add_trackings
  4034-4074   bulk_delete_archive_entries
  7758-7817   bulkadd
  9129-9269   check_all_trackings
  4630-4642   claim_live_transition
 22141-22887  class KickModerator
 20847-21825  class RestreamManager
 13158-13200  classify_proxy_anonymity
  6999-7197   cleanup
  5962-6003   cleanup_old_recordings
  4776-4783   clear_recording
 31715-31780  clip_moment
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
 33088-33149  einnahmen_cmd
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
  9973-10583  handle_recording_finished
  3916-3941   init_db
  5784-5838   inspect_stream_url
 26578-26580  is_revenue_platform
  5242-5250   list_archive_rules
  6232-6270   live
  8669-8677   live_check_worker
  3524-3558   llm_chat
  3623-3690   llm_chat_stream_sync
  3592-3620   llm_chat_sync
  3577-3589   llm_list_models
  4837-4863   log_event
  1381-1414   log_recording_failure
  8074-8123   logs_cmd
 33755-34200  main
  6927-6950   on_ai_media
  8200-8226   on_ai_reply
  8229-8258   on_azrael_mention
  8290-8320   on_callback
 23297-23401  oracle_handle
  7963-7966   pause_tracking
  6092-6097   profile_keyboard
  5745-5781   quick_restart_tracking
  8025-8071   quota
  9046-9109   reaper_loop
  5366-5368   record_tiktok_status
  6966-6996   recstatus
  3474-3482   redis_get_json
  3484-3490   redis_set_json
  4545-4569   remove_tracking
  4899-4910   remove_tracking_tag
  4089-4224   rename_archive_entry
 33152-33162  report_cmd
 13203-13205  report_proxy_result
  2154-2181   resolve_tiktok_live_stream
  5614-5617   restore_recording
  7969-7972   resume_tracking
  5280-5360   run_archive_rules
 33165-33370  run_bot
 16743-16790  run_flask
  5158-5203   sample_bandwidth_for_active
  5209-5228   save_profile_snapshot
  4374-4380   save_tiktok_check
  4768-4774   set_recording_file
  4588-4626   set_tracking_paused
  4935-4964   set_tracking_priority
  5609-5612   soft_delete_recording
  9358-9971   split_and_send_video
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
