# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (255)

```
 10636  GET              /                                                dashboard
 15526  GET              /api/abo/status                                  api_abo_status
 10735  GET              /api/active-recordings                           api_active_recordings
 15601  GET              /api/activity-pulse                              api_activity_pulse
 14954  GET              /api/ai-log                                      api_ai_log
 11133  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15361  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23312  GET/POST         /api/audio/config                                api_audio_config
 23342  POST             /api/audio/testtone                              api_audio_testtone
 15467  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15491  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15495  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12411  GET              /api/automation/status                           api_automation_status
 12433  POST             /api/automation/toggle                           api_automation_toggle
 14159  GET              /api/azrael/agents                               api_azrael_agents
 12314  POST             /api/azrael/ask                                  api_azrael_ask
 23548  GET/POST         /api/azrael/context                              api_azrael_context
 13786  GET              /api/azrael/core                                 api_azrael_core
 23682  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23672  GET              /api/azrael/live_status                          api_azrael_live_status
 23690  POST             /api/azrael/live_test                            api_azrael_live_test
 14168  GET              /api/azrael/memories                             api_azrael_memories
 23738  POST             /api/azrael/persona                              api_azrael_persona_set
 23729  GET              /api/azrael/personas                             api_azrael_personas
 23766  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23521  POST             /api/azrael/react                                api_azrael_react
 23557  GET              /api/azrael/reaction                             api_azrael_reaction
 23709  GET              /api/azrael/reactions                            api_azrael_reactions
 23759  GET              /api/azrael/transcript                           api_azrael_transcript
 23644  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23619  GET              /api/azrael/voices                               api_azrael_voices
 23783  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11228  GET              /api/backoff-watch                               api_backoff_watch
 14725  POST             /api/backup/run                                  api_backup_run
 14691  GET              /api/backup/status                               api_backup_status
 14680  POST             /api/backup/system                               api_backup_system
 15433  GET              /api/bandwidth/live                              api_bandwidth_live
 15346  GET              /api/bookmarks                                   api_bookmarks_list
 11491  GET              /api/brain                                       api_brain
 11428  GET              /api/brain/alarms                                api_brain_alarms
 11413  GET              /api/brain/creator                               api_brain_creator
 11390  GET              /api/brain/graph                                 api_brain_graph
 11451  GET              /api/brain/growth                                api_brain_growth
 10190  GET              /api/brain/health                                api_brain_health
 24264  GET              /api/channel/categories                          api_channel_categories
 24270  POST             /api/channel/set                                 api_channel_set
 24080  GET              /api/channels/status                             api_channels_status
 22913  POST             /api/chat/send                                   api_chat_send
 14426  GET              /api/chat/send_status                            api_chat_send_status
 10716  GET              /api/checks                                      api_checks
 23585  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23568  GET              /api/clips                                       api_clips
 23601  POST/DELETE      /api/clips/clear                                 api_clips_clear
 23187  GET              /api/cohost                                      api_cohost
 23199  POST             /api/cohost/config                               api_cohost_config
 16165  GET              /api/community/stats                             api_community_stats
 25264  POST             /api/config/restore                              api_config_restore
 25249  GET              /api/config/snapshot                             api_config_snapshot
 15624  GET              /api/cookies/age                                 api_cookies_age
 10783  GET              /api/cookies/health                              api_cookies_health
 10790  POST             /api/cookies/update                              api_cookies_update
 25215  GET              /api/data/export                                 api_data_export
 16680  GET              /api/db/export                                   api_db_export
 16707  POST             /api/db/import                                   api_db_import
 16667  GET              /api/db/summary                                  api_db_summary
 23113  GET              /api/debug/threads                               api_debug_threads
 26150  GET              /api/defense/attacks                             api_defense_attacks
 26117  GET              /api/defense/crowdsec                            api_defense_crowdsec
 26135  GET              /api/defense/fail2ban                            api_defense_fail2ban
 25841  GET              /api/defense/overview                            api_defense_overview
 14787  POST             /api/discord/announce                            api_discord_announce
 14515  GET              /api/discord/clips_week                          api_discord_clips_week
 14731  GET              /api/discord/community                           api_discord_community
 14454  GET              /api/discord/invite                              api_discord_invite
 13917  GET              /api/discord/overview                            api_discord_overview
 14003  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16242  POST             /api/donations/add                               api_donations_add
 16275  GET              /api/donations/manual                            api_donations_manual
 16283  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16178  POST             /api/donations/reset                             api_donations_reset
 16299  GET              /api/donations/summary                           api_donations_summary
 15415  GET              /api/events                                      api_events
 14562  GET              /api/events/stream                               api_events_stream
 17335  GET              /api/evolution/changelog                         api_evolution_changelog
 17320  GET              /api/evolution/history                           api_evolution_history
 17260  GET              /api/evolution/learned                           api_evolution_learned
 17282  GET              /api/evolution/proposals                         api_evolution_proposals
 17303  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17250  POST             /api/evolution/run                               api_evolution_run
 17350  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17215  GET              /api/evolution/status                            api_evolution_status
 16514  GET              /api/finanzamt/entries                           api_finanzamt_entries
 16534  POST             /api/finanzamt/entry                             api_finanzamt_add
 16561  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15428  GET              /api/forecast/storage                            api_forecast_storage
 12449  GET              /api/freeai/status                               api_freeai_status
 13859  GET              /api/health                                      api_health
 15446  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15442  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23236  GET              /api/highlights                                  api_highlights
 23248  POST             /api/highlights/config                           api_highlights_config
 24121  GET              /api/kick/channel                                api_kick_channel
 24142  POST             /api/kick/channel                                api_kick_channel_set
 13586  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13654  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13632  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13571  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13611  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23360  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23429  POST             /api/kickmod/config                              api_kickmod_config
 23474  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23488  GET              /api/kickmod/learned                             api_kickmod_learned
 23515  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23495  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 23826  POST             /api/kickmod/say                                 api_kickmod_say
 23802  POST             /api/kickmod/start                               api_kickmod_start
 23400  GET              /api/kickmod/status                              api_kickmod_status
 23813  POST             /api/kickmod/stop                                api_kickmod_stop
 10570  POST             /api/login                                       dashboard_login_submit
 16150  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12864  POST             /api/marketing/config                            api_marketing_config
 12889  GET              /api/marketing/preview                           api_marketing_preview
 12899  POST             /api/marketing/send-now                          api_marketing_send_now
 12838  GET              /api/marketing/status                            api_marketing_status
 12856  POST             /api/marketing/toggle                            api_marketing_toggle
 23263  GET              /api/moderation/feed                             api_moderation_feed
 13417  POST             /api/news/config                                 api_news_config
 13383  GET              /api/news/creators                               api_news_creators
 13394  POST             /api/news/creators/generate                      api_news_creators_generate
 13459  POST             /api/news/generate-now                           api_news_generate_now
 13454  GET              /api/news/items                                  api_news_items
 13445  GET              /api/news/preview                                api_news_preview
 13364  GET              /api/news/status                                 api_news_status
 13409  POST             /api/news/toggle                                 api_news_toggle
 16007  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14391  GET              /api/notify/status                               api_notify_status
 14402  POST             /api/notify/test                                 api_notify_test
 14377  GET              /api/ops/audit                                   api_ops_audit
 16078  GET              /api/ops/db-stats                                api_ops_db_stats
 16106  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14183  GET              /api/ops/errors                                  api_ops_errors
 16027  GET              /api/ops/healthcheck                             api_ops_healthcheck
 16762  GET              /api/ops/log-tail                                api_ops_log_tail
 12294  GET              /api/ops/logtail                                 api_ops_logtail
 14124  GET              /api/ops/metrics                                 api_ops_metrics
 14107  GET              /api/ops/resource_history                        api_ops_resource_history
 16736  GET              /api/ops/version                                 api_ops_version
 10986  GET              /api/outcomes                                    api_outcomes
 24745  POST             /api/overlay/config                              api_overlay_config
 24732  POST             /api/overlay/event                               api_overlay_event
 24637  GET              /api/overlay/state                               api_overlay_state
 11019  GET              /api/profile/<username>                          api_profile
 15632  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15454  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15580  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15557  GET              /api/proxy/trend                                 api_proxy_trend
 13338  GET              /api/public/stats                                api_public_stats
 10670  GET              /api/pulse                                       api_pulse
 14978  GET              /api/recording-attempts                          api_recording_attempts
 22848  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 22826  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 22867  POST             /api/restream/<int:rid>/start                    api_restream_start
 23134  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24599  GET              /api/restream/chatfeed                           api_restream_chatfeed
 22802  POST             /api/restream/create                             api_restream_create
 13662  GET              /api/restream/deck                               api_restream_deck
 12385  GET              /api/restream/health                             api_restream_health
 24621  POST             /api/restream/layout                             api_restream_layout
 22775  GET              /api/restream/list                               api_restream_list
 12358  POST             /api/restream/report                             api_restream_report
 23147  POST             /api/restream/start_all                          api_restream_start_all
 23173  POST             /api/restream/stop_all                           api_restream_stop_all
 12612  GET              /api/restream/testpush                           api_testpush_status
 12637  POST             /api/restream/testpush                           api_testpush_run
 16415  GET              /api/restream/verify                             api_restream_verify
 14493  GET              /api/retention/preview                           api_retention_preview
 14502  POST             /api/retention/run                               api_retention_run
 25330  POST             /api/schedule/add                                api_schedule_add
 25320  GET              /api/schedule/list                               api_schedule_list
 25355  POST             /api/schedule/remove                             api_schedule_remove
 15331  GET              /api/search                                      api_search
 25888  GET              /api/selftest                                    api_selftest
 22884  GET              /api/shield/stats                                api_shield_stats
 10689  GET              /api/stats                                       api_stats
 15595  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15522  GET              /api/stats/tiktok-status                         api_tiktok_status
 25295  GET              /api/stats/timeline                              api_stats_timeline
 10757  GET              /api/storage                                     api_storage
 10764  POST             /api/storage/cleanup                             api_storage_cleanup
 15508  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12335  GET              /api/stream/timeline                             api_stream_timeline
 13991  GET              /api/stream/transcript                           api_stream_transcript
 24963  GET              /api/streamer/compare                            api_streamer_compare
 25162  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14467  GET              /api/streamer/detail                             api_streamer_detail
 25187  GET              /api/streamer/digest/<username>                  api_streamer_digest
 25067  GET              /api/streamer/dormant                            api_streamer_dormant
 25143  GET              /api/streamer/exists/<username>                  api_streamer_exists
 25022  GET              /api/streamer/journal/<username>                 api_streamer_journal
 24987  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 25047  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13826  GET              /api/streamers/wall                              api_streamers_wall
 10906  GET              /api/summary/preview                             api_summary_preview
 15043  GET              /api/system                                      api_system
 16363  GET              /api/system/check_timing                         api_check_timing
 16648  GET              /api/system/config_drift                         api_config_drift
 14027  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14238  GET              /api/system/preflight                            api_system_preflight
 14364  GET              /api/system/preflight_history                    api_system_preflight_history
 14627  GET              /api/system/resilience                           api_system_resilience
 15366  GET              /api/tags                                        api_tags_list
 10730  GET              /api/top                                         api_top
 12268  GET              /api/trackings                                   api_trackings
 15896  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 15929  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15615  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 15958  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 14817  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 14864  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 14893  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 14875  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10923  POST             /api/trackings/bulk                              api_trackings_bulk
 14832  GET              /api/trackings/export                            api_trackings_export
 15370  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15670  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11283  GET              /api/trend-7d                                    api_trend_7d
 23633  GET              /api/tts/<fn>                                    api_tts_file
 12492  POST             /api/tunnel/set                                  api_tunnel_set
 12471  GET              /api/tunnel/status                               api_tunnel_status
 12503  POST             /api/tunnel/test                                 api_tunnel_test
 12484  POST             /api/tunnel/toggle                               api_tunnel_toggle
 16620  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16597  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16579  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 24773  GET              /api/upload_window                               api_upload_window
 11000  GET              /api/userstats                                   api_userstats
 13470  GET              /api/version                                     api_version
 16476  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16497  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16461  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16445  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 29568  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15016  GET              /archive/<int:eid>/download                      archive_download
 15073  GET              /download/<int:recording_id>                     download
 14939  GET              /health                                          health
 23082  GET              /healthz                                         healthz
 10561  GET              /login                                           dashboard_login_page
 10591  GET              /logout                                          dashboard_logout
 10598  GET              /manifest.webmanifest                            pwa_manifest
 14055  GET              /metrics                                         api_prometheus_metrics
 24582  GET              /overlay                                         overlay_page
 10622  GET              /pwa-icon-<variant>.png                          pwa_icon
 10608  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (90)

```
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   814  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   896  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   924  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   935  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   801  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   863  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   850  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   831  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   476  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   471  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   519  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   402  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   729  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   493  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   456  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   429  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   573  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   662  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   568  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   501  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   281  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   746  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   369  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   624  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   779  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   764  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   325  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   563  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   549  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   532  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   589  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   682  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   578  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 26593  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 27052  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 26684  /assign_role            Rolle/Gruppe einem Mitglied geben
 26730  /ban                    Mitglied bannen
 27384  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 27308  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27348  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 27333  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 27175  /clips                  Letzte Highlight-Clips eines Users
 26645  /create_category        Kategorie anlegen
 26614  /create_channel         Text-Channel anlegen (optional in Kategorie)
 26673  /create_group           Nutzergruppe (= Rolle) anlegen
 26656  /create_role            Rolle / Nutzergruppe anlegen
 26630  /create_voice           Voice-Channel anlegen
 26966  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 27082  /event                  Community-Event ankündigen (Admin) — mit Countdown
 27125  /events                 Kommende Community-Events anzeigen
 27221  /follow                 Bei Live-Gang eines Streamers gepingt werden
 27205  /help                   Alle Bot-Befehle anzeigen
 26719  /kick                   Mitglied kicken
 26948  /leaderboard            Top-10 der Community nach XP
 27161  /livenow                Welche getrackten User sind gerade live
 27191  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 27022  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 26754  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 26934  /rank                   Dein Level und Rang anzeigen
 27148  /recstatus              Aktuell laufende Aufnahmen
 26695  /remove_role            Rolle/Gruppe entfernen
 26607  /restream_status        Restream-Status
 26706  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 26899  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 26917  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 27247  /stats                  Statistik zu einem getrackten Streamer
 26519  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 27543  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 27440  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 27416  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 26741  /timeout                Mitglied stummschalten (Minuten)
 27319  /topstreamers           Rangliste der Streamer nach Aufnahmen
 26549  /track                  TikTok-User tracken
 26533  /tracklist              Getrackte TikTok-User dieses Servers
 27236  /unfollow               Live-Pings für einen Streamer abbestellen
 26582  /untrack                TikTok-User nicht mehr tracken
 27269  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 27293  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 28027  on_member_join
 27989  on_message
 27630  on_raw_reaction_add
 28062  on_ready
```

## Top-Level-Symbole in bot_v37.py (554 Funktionen, 2 Klassen)

```
  2446-2447   _abo_key
  2467-2485   _abo_probe_dump
 25430-25440  _active_recorder_sync
 20072-20079  _ad_allowlist
 21194-21200  _agent_for
 25442-25460  _ai_calls_total_sync
 21203-21219  _ai_telemetry
 21701-21719  _alert
 28175-28225  _alert_monitor_loop
 28599-28661  _announce_loop
  3388-3391   _anthropic_key
  3398-3400   _anthropic_model
 10318-10321  _arg_int
  2438-2443   _as_dict
 17932-17937  _audio_cfg
 21855-21877  _audio_tap_cmd
 10482-10493  _auth_cookie
 10449-10478  _auth_guard
  1594-1599   _auto_on
 22751-22769  _auto_restream_loop
 29729-29744  _azrael_broadcast_reply
 29629-29651  _azrael_chat_reply
 29612-29626  _azrael_chat_should_reply
 13064-13082  _azrael_creator_take
 29657-29659  _azrael_gate_cfg
 21224-21238  _azrael_live_state
 24481-24495  _azrael_overlay_state
 21584-21638  _azrael_proactive_loop
 21043-21099  _azrael_reaction_to_chats
 29662-29669  _azrael_reply_all_chats
 29599-29609  _azrael_self_names
 29697-29726  _azrael_send_to
 21241-21262  _azrael_system
 28339-28342  _backup_active
 28420-28433  _backup_loop
 19960-19961  _badwords_path
 28140-28149  _brain_growth_loop
 11359-11386  _brain_growth_snapshot
  2374-2394   _brain_hint_delay
 11351-11353  _brain_history_for
  6810-6838   _brain_notify
 11328-11349  _brain_record
 11355-11357  _brain_stream_recent
 14541-14558  _browser_push
  6854-6941   _build_daily_summary
  2877-3057   _build_native_cmd
 18280-18467  _build_restream_cmd
  3101-3134   _build_ytdlp_cmd
 25382-25389  _cached_probe
  5632-5659   _can_stop_tracking
  1774-1796   _capture_set_cookies
 15718-15721  _cfg_get
 15724-15726  _cfg_set
 24225-24260  _channel_set_all
 17530-17533  _chat_connected
 17536-17552  _chat_disconnected
  8883-8894   _chat_is_forum
 17572-17574  _chat_sanitize
 17576-17585  _chat_src_ok
 17515-17527  _chat_stat
 17555-17558  _chat_stats_snapshot
  3663-3674   _check_ai_alive_sync
  3677-3689   _check_ai_models_sync
 25391-25404  _check_redis_alive_sync
 25406-25426  _check_redis_version_sync
 11958-12001  _classify_pool_anonymity
 12004-12021  _classify_pool_anonymity_bg
   774-778    _claude_chat_sync_metered
 10343-10350  _client_ip
 28693-28720  _clip_prune
 28723-28733  _clip_recfile_for
 29249-29255  _clip_should_velocity
 28774-28856  _clip_to_discord
  3561-3570   _close_ai_session
 29773-29788  _cohost_broadcast
 29755-29759  _cohost_cfg
 29814-29826  _cohost_fire_highlight
 29762-29770  _cohost_gate
 29791-29811  _cohost_highlight
 28905-28939  _community_events_loop
 11182-11184  _conv_messages
  7234-7274   _cookie_alarm_loop
  1846-1850   _cookie_autorefresh_info
  1751-1755   _cookie_header
 14591-14623  _cpu_load_snapshot
  3871-3883   _create_index_safe
 13032-13047  _creator_activity
 13088-13111  _creator_dossier_generate
 13050-13061  _creator_facts_line
 25643-25749  _crowdsec_status
 25609-25640  _crowdsec_via_lapi
 25474-25492  _cscli_bin
 25498-25511  _cscli_path
  7127-7152   _daily_summary_loop
 25529-25546  _darf_journal_lesen
 28152-28172  _db_maintenance_loop
  7099-7124   _db_vacuum_loop
 20095-20119  _detect_foreign_ad
  1351-1362   _diag_path_owner
 21490-21534  _director_finalize
 22301-22308  _director_for
 21439-21487  _director_mark
 29143-29178  _disc_automod_check
 29116-29122  _disc_state_get
 29125-29132  _disc_state_set
 26192-26205  _discord_guild_filesize_bytes
 26391-26400  _discord_invite
 29077-29113  _discord_live_thread
 21641-21653  _discord_notify
 26292-26317  _discord_ops_alert
 28975-29073  _discord_post_user
 26456-28137  _discord_run_once
 26330-26388  _discord_start
 28664-28670  _discord_stop
 26213-26215  _discord_upload_limit_label
 26208-26210  _discord_upload_limit_mb
  7155-7229   _disk_alarm_loop
 31045-31094  _disk_autoclean
 31097-31110  _disk_guard_loop
 31037-31042  _disk_pct
 24538-24541  _donations_unknown_count
 17889-17891  _drawtext_chain
 15170-15172  _dump_all_threads
 11883-11947  _enrich_proxies_with_geo
  1991-2035   _ensure_cookie_file_netscape
 26403-26453  _ensure_discord_invite
 28870-28902  _ensure_error_channel
 12126-12163  _ensure_proxy_ready
  8896-8919   _ensure_topic
   637-639    _env_int
   642-644    _env_int_range
 28942-28972  _error_channel_loop
 21685-21698  _event_webhook
 16823-16829  _evo_build_dir
 16832-16839  _evo_version
 17115-17196  _evolution_cycle
 16848-16868  _evolution_llm_note
 17199-17209  _evolution_loop
 16871-17112  _evolution_write_build
  6252-6286   _extract_file_payload
  2123-2125   _extract_urls_from_streamurl_node
 25514-25521  _f2b_sudo_hint
 21721-21723  _faster_whisper_available
 19984-19996  _fetch_ldnoobw_de
 11772-11790  _fetch_proxy_list
 22135-22163  _fetch_tiktok_room_id
   708-711    _ff_cmd
 15841-15854  _ffmpeg_version_str
 18052-18057  _find_chromium
  3094-3098   _find_external_recorder
  2128-2130   _find_stream_urls
 15769-15794  _fire_webhooks
  8010-8019   _fork_safe
   789-798    _freeai_chat_sync_metered
 25564-25606  _geo_lookup_ips
  3550-3559   _get_ai_session
  7844-7884   _get_live_info
  2664-2671   _get_resolve_semaphore
  8245-8610   _handle_single_tracking
 30889-30891  _hb
 30894-30911  _hb_while
 17590-17592  _highlight_cfg
 17595-17624  _highlight_observe
 18060-18065  _htmlov_screenshot_cmd
 21879-21889  _httpx_proxy
 15802-15814  _in_quiet_hours
 31878-31909  _install_fast_eventloop
 10213-10267  _install_fast_json
 15175-15191  _install_faulthandler
 22994-23003  _intel_ensure_schema
 23041-23072  _intel_index_loop
 23015-23025  _intel_index_one
 23006-23012  _intel_semantic
  5621-5630   _is_authorized
  8175-8181   _is_dead
  2113-2115   _is_hevc
 25549-25555  _is_private_ip
  1497-1504   _is_process_running
  6840-6851   _is_quiet_hours
  1159-1168   _is_upload_window
 10302-10315  _json_error_handler
  7057-7087   _kick_broadcaster_id
 12538-12557  _kick_channel_live
  6974-7016   _kick_follower_count
 13549-13562  _kick_oauth_exchange
 13565-13567  _kick_oauth_page
 13508-13512  _kick_redirect_public
 13499-13505  _kick_redirect_source
 13485-13496  _kick_redirect_uri
  6959-6961   _kick_slug
 13515-13546  _kick_user_token
  3920-3923   _kind_from_filename
 15831-15836  _latest_popularity
 20006-20012  _learned_load
 20003-20004  _learned_path
 20014-20022  _learned_save
 22516-22546  _live_react_loop
 22312-22505  _live_react_worker
 21102-21113  _live_transcript_push
 22507-22514  _live_users
 21537-21581  _living_title_loop
 19963-19971  _load_banned_words_file
  1672-1745   _load_cookies_dict
 28345-28417  _local_backup_scan
 10284-10298  _log_5xx
 18475-18487  _looks_like_codec_err
 18470-18472  _looks_like_source_expired
  8091-8121   _loop_fehler
 15195-15204  _loop_heartbeat
 30859-30886  _loop_lag_monitor
 15314-15317  _loop_not_ready
 15207-15275  _loop_watchdog_thread
 20982-20996  _loyalty_add
 20973-20979  _loyalty_get
 20999-21007  _loyalty_top
 16215-16233  _manual_donations_rows
 16236-16238  _manual_donations_total
  8183-8184   _mark_dead
 12705-12734  _marketing_cfg
 12696-12702  _marketing_default_targets
 12691-12693  _marketing_enabled
 12748-12763  _marketing_flavor
 12818-12834  _marketing_loop
 12766-12776  _marketing_post_discord
 12779-12791  _marketing_post_telegram
 12794-12815  _marketing_publish
 12737-12741  _marketing_state_obj
 12744-12745  _marketing_state_save
 29676-29694  _maybe_handle_command
 31196-31220  _maybe_hype_clip
  3838-3861   _migrate_columns
 29953-29964  _mod_is_exempt
 29967-29972  _mod_warn_first
 29975-29978  _mod_warn_text
 17378-17386  _modlog
   912-914    _multistream_targets
  8022-8023   _nc_create_subprocess_exec
  8026-8027   _nc_create_subprocess_shell
 12929-12945  _news_cfg
 12916-12918  _news_enabled
 12983-13024  _news_facts
 13138-13160  _news_generate
 13343-13360  _news_loop
 12921-12926  _news_output_path
 13027-13029  _news_phrase
 13114-13135  _news_phrase_impl
 12958-12965  _news_read
 12948-12951  _news_state_obj
 12954-12955  _news_state_save
 12968-12980  _news_write
 17416-17418  _normalize_ingest
  2305-2322   _note_check_duration
 21128-21136  _oracle_memories
 21394-21428  _oracle_memorize
 21139-21152  _oracle_persona
 21121-21125  _oracle_recent_text
 17715-17723  _ov_atomic_write
 17703-17709  _ov_bar
 19919-19931  _ov_clip_text
 17712-17713  _ov_oneline
 24549-24578  _overlay_push
 18006-18049  _overlay_render_size
 17477-17481  _overlay_session_reset
 24497-24500  _overlay_src_ok
 20082-20092  _own_invites
 16196-16212  _parse_eur
 18001-18003  _parse_size
 25757-25837  _parse_ssh_attacks
  7446-7479   _pause_resume_cmd
  1800-1844   _persist_refreshed_cookies
  1638-1670   _pick_checked_pull_proxy
 10379-10392  _pin_auth_value
 10438-10439  _pin_clear_fail
 10418-10421  _pin_locked
 10424-10435  _pin_note_fail
 10395-10415  _pin_ok
 24387-24389  _piper_available
 24352-24374  _piper_list_voices
 24394-24419  _piper_pick_model
 24431-24478  _piper_say
 24345-24349  _piper_voice_roots
 15731-15766  _post_json_threaded
 17980-17998  _probe_video_size
  1525-1542   _proc_is_recorder
 11870-11881  _proxy_geo_cache_put
 12097-12123  _proxy_pool_refresh_loop
  1604-1635   _proxy_report_recording
 15160-15162  _prune_stall_dumps
 13163-13284  _public_stats
 21656-21682  _push_notify
 10540-10542  _pwa_dir
 11841-11856  _quick_validate_proxy
 15797-15799  _quiet_hours_config
 10505-10538  _rate_guard
 20947-20953  _react_warn
  7930-7969   _reap_proc
  2345-2367   _record_check_outcome
   703-705    _redact_stream_urls
 12024-12094  _refresh_proxy_pool
 24377-24383  _resolve_piper_model
  2139-2229   _resolve_via_html
  2487-2641   _resolve_via_webcast_api_v2
  2704-2766   _resolve_via_ytdlp
 29295-29424  _resolve_youtube_ingest
 22585-22592  _restream_active_platforms
 17462-17473  _restream_active_sources
 22166-22265  _restream_chat_guardian
 17627-17699  _restream_chat_push
 17389-17401  _restream_enabled
 18068-18155  _restream_html_overlay_start
 18158-18171  _restream_html_overlay_stop
  1107-1109   _restream_layout_mode
 17427-17450  _restream_overlay_files
 22550-22582  _restream_platform_state
 22713-22748  _restream_resume_after_restart
 18219-18277  _restream_tts_enqueue_wav
 17942-17974  _restream_tts_feeder
 17939-17940  _restream_tts_fifo_path
 18174-18201  _restream_tts_start
 18203-18217  _restream_tts_stop
 22595-22710  _restream_verify_loop
 28310-28322  _retention_loop
 28269-28307  _retention_scan
  2449-2451   _room_is_abo
  6290-6407   _run_ai_call
 15298-15311  _run_async_from_flask
 25558-25561  _run_priv
 31866-31874  _run_selfcheck_and_exit
 28325-28336  _s3_client
  8186-8232   _safe_send
  4773-4789   _sample_net_throughput
 19973-19981  _save_banned_words_file
  2397-2424   _schedule_next_check
 28228-28266  _scheduler_loop
  3864-3868   _schema_pk
 15319-15324  _scraper_session
 29981-30020  _screen_full
 13875-13912  _sec_headers
  2118-2120   _select_stream_from_data_section
 31679-31863  _selfcheck
  1182-1186   _should_defer_upload
 28736-28771  _shrink_for_discord
 10545-10557  _sicheres_ziel
 31117-31134  _sign_health_check
 31137-31156  _sign_health_loop
  8039-8050   _spawn
  8053-8083   _spawn_from_flask
 25881-25884  _st_befund
 21891-22132  _start_chat_listener
 15278-15295  _start_loop_watchdog
 13308-13334  _stats_loop
 13287-13290  _stats_output_path
 13293-13305  _stats_write
  8678-8692   _storage_cleanup_loop
 31176-31183  _story_for
  3156-3162   _stream_url_expiry
  3171-3177   _stream_url_is_fresh
  3164-3169   _stream_url_ttl
 20046-20053  _streamer_persona_get
 20028-20034  _streamer_personas_load
 20025-20026  _streamer_personas_path
 20036-20044  _streamer_personas_save
 17894-17898  _studio_chain
 28442-28564  _system_backup
 28567-28595  _system_backup_loop
 11793-11832  _test_proxy
 12579-12588  _testpush_cfg
 12591-12608  _testpush_exec
 12560-12576  _testpush_resolve_live
  8855-8865   _tg_topics_load_into_mem
  8852-8853   _tg_topics_path
  8867-8874   _tg_topics_save
 25091-25139  _tiktok_account_exists
 10353-10361  _token_ok
  8877-8881   _topic_forget
 15817-15828  _tracking_max_duration
  1409-1432   _try_attach_file_handler
 24421-24429  _tts_cleanup
 12464-12467  _tunnel_effective
 23847-23900  _twitch_channel_status
 30023-30166  _twitch_chat_loop
 29837-29940  _twitch_eventsub_loop
 16641-16644  _twitch_oauth_page
  1205-1218   _upload_queue_add
  1229-1231   _upload_queue_count
  1188-1197   _upload_queue_load
  1178-1180   _upload_queue_path
  1220-1227   _upload_queue_remove
  1199-1203   _upload_queue_save
  1233-1271   _upload_window_loop
  7903-7910   _uptime_s
 17404-17413  _url_host
   683-700    _url_ohne_zugang
   767-771    _usage_record_claude
  8124-8168   _verbindung_verloren
  7019-7047   _viewer_sample_loop
  7089-7096   _viewer_stats
 10442-10445  _wants_html
  7913-7927   _warn_empty_env
 30932-31027  _watchdog_loop
 29578-29586  _wchat_thank_ok
 21725-21755  _whisper_get_model
  8000-8007   _whisper_native_section
 20934-20940  _whisper_pool
 21824-21853  _whisper_segments
 21757-21821  _whisper_transcribe
 17725-17887  _write_restream_overlay
 30194-30267  _youtube_api_chat_loop
 23903-24006  _youtube_api_status
 24009-24076  _youtube_channel_status
 30270-30427  _youtube_chat_loop
 29430-29443  _youtube_restream_autoconfig
 29446-29470  _youtube_restream_autoconfig_inner
 29536-29564  _youtube_send
 24181-24222  _youtube_set_channel
 29473-29507  _yt_access_token
 29510-29525  _yt_live_chat_id
 30187-30191  _yt_oauth_configured
 29531-29533  _yt_sendrate_cfg
 30169-30184  _yt_timeout
  2688-2689   _ytdlp_detect_available
  2691-2702   _ytdlp_note_result
 15165-15167  _zombie_child_count
  7780-7804   about
  4039-4043   add_ai_log_entry
  3956-3959   add_archive_entry
  4886-4901   add_archive_rule
  4468-4502   add_recording
  4129-4146   add_tracking
  4563-4580   add_tracking_tag
  6410-6443   ai
  3703-3742   ai_chat
  3776-3786   ai_history_append
  3788-3793   ai_history_clear
  3765-3774   ai_history_load
  3750-3763   ai_rate_limit_check
  6472-6480   aireset
 21265-21284  azrael_chat
 30432-30554  brain_cmd
  3180-3364   build_recording_cmd
  4149-4226   bulk_add_trackings
  7277-7336   bulkadd
  8695-8835   check_all_trackings
  4313-4325   claim_live_transition
 20122-20877  class KickModerator
 18490-19806  class RestreamManager
 12208-12250  classify_proxy_anonymity
  6518-6716   cleanup
  5481-5522   cleanup_old_recordings
  4459-4466   clear_recording
 29181-29246  clip_moment
  5034-5077   cluster_failures
  4717-4766   compute_storage_forecast
  7399-7443   cookies_cmd
  5323-5329   cookies_days_old
  4120-4126   count_trackings_for_chat
  4026-4037   decide_preferred_recorder
  3966-3969   delete_archive_entry
  4903-4911   delete_archive_rule
  5947-6094   diag
 30557-30618  einnahmen_cmd
  4711-4714   find_recordings_by_fingerprint
  3987-4003   finish_recording_attempt
  4258-4268   get_all_active_trackings
  4065-4068   get_all_checks
  4504-4507   get_all_recordings
  4605-4615   get_all_tags_with_counts
  4688-4691   get_annotations_for_recording
  3961-3964   get_archive_entry
  4681-4684   get_bookmarked_recordings
  1867-1984   get_cookie_health
  4554-4560   get_event_log
  4010-4024   get_last_recording_attempt
  2769-2874   get_live_status
  5237-5240   get_manual_recordings
  4696-4699   get_or_compute_inspect_sync
  5557-5601   get_outcome_breakdown
  4662-4670   get_priority_poll_interval
  4864-4873   get_profile_snapshots
  4045-4055   get_recent_ai_log
  4005-4008   get_recent_recording_attempts
  4509-4512   get_recording_by_id
  4674-4677   get_recording_note
  3498-3521   get_redis
  4096-4112   get_stats
  5448-5479   get_storage_stats
  4595-4603   get_tags_for_tracking
  5004-5018   get_tiktok_status_distribution
  4649-4660   get_tracking_priority
  4327-4336   get_tracking_state
  4254-4256   get_trackings_for_group
  5253-5256   get_trash_recordings
  9539-10181  handle_recording_finished
  3886-3911   init_db
  5371-5425   inspect_stream_url
 24544-24546  is_revenue_platform
  4876-4884   list_archive_rules
  5751-5789   live
  8235-8243   live_check_worker
  3573-3607   llm_chat
  3630-3658   llm_chat_sync
  3615-3627   llm_list_models
  4520-4546   log_event
  1459-1492   log_recording_failure
  7593-7642   logs_cmd
 31224-31669  main
  6446-6469   on_ai_media
  7719-7745   on_ai_reply
  7748-7777   on_azrael_mention
  7809-7839   on_callback
 21287-21391  oracle_handle
  7482-7485   pause_tracking
  5611-5616   profile_keyboard
  5332-5368   quick_restart_tracking
  7544-7590   quota
  8612-8675   reaper_loop
  5000-5002   record_tiktok_status
  6485-6515   recstatus
  3523-3531   redis_get_json
  3533-3539   redis_set_json
  4228-4252   remove_tracking
  4582-4593   remove_tracking_tag
 30621-30631  report_cmd
 12253-12255  report_proxy_result
  2232-2259   resolve_tiktok_live_stream
  5248-5251   restore_recording
  7488-7491   resume_tracking
  4914-4994   run_archive_rules
 30634-30839  run_bot
 15087-15134  run_flask
  4792-4837   sample_bandwidth_for_active
  4843-4862   save_profile_snapshot
  4057-4063   save_tiktok_check
  4451-4457   set_recording_file
  4271-4309   set_tracking_paused
  4618-4647   set_tracking_priority
  5243-5246   soft_delete_recording
  8924-9537   split_and_send_video
  5664-5706   start
  3971-3985   start_recording_attempt
  6719-6757   stats
  5218-5235   stop_manual_recording
  7494-7541   stoprec
  6944-6952   summary_cmd
  7645-7716   sysres
  6096-6240   teststream
  5708-5749   tiktok
  7339-7396   topusers
  5826-5883   track
  5791-5823   track_exact
  5897-5945   tracklist
  5084-5216   trigger_manual_recording
  4412-4449   try_acquire_recording_lock
  5259-5318   universal_search
  5885-5895   untrack
  4706-4709   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
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
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
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
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
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
