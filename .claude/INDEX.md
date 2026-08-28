# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (226)

```
 10739  GET              /                                                dashboard
 15544  GET              /api/abo/status                                  api_abo_status
 10847  GET              /api/active-recordings                           api_active_recordings
 15619  GET              /api/activity-pulse                              api_activity_pulse
 14972  GET              /api/ai-log                                      api_ai_log
 11207  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15379  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 22978  GET/POST         /api/audio/config                                api_audio_config
 23008  POST             /api/audio/testtone                              api_audio_testtone
 15485  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15509  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15513  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12478  GET              /api/automation/status                           api_automation_status
 12500  POST             /api/automation/toggle                           api_automation_toggle
 14193  GET              /api/azrael/agents                               api_azrael_agents
 12370  POST             /api/azrael/ask                                  api_azrael_ask
 23214  GET/POST         /api/azrael/context                              api_azrael_context
 13868  GET              /api/azrael/core                                 api_azrael_core
 23348  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23338  GET              /api/azrael/live_status                          api_azrael_live_status
 23356  POST             /api/azrael/live_test                            api_azrael_live_test
 14202  GET              /api/azrael/memories                             api_azrael_memories
 23404  POST             /api/azrael/persona                              api_azrael_persona_set
 23395  GET              /api/azrael/personas                             api_azrael_personas
 23432  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23187  POST             /api/azrael/react                                api_azrael_react
 23223  GET              /api/azrael/reaction                             api_azrael_reaction
 23375  GET              /api/azrael/reactions                            api_azrael_reactions
 23425  GET              /api/azrael/transcript                           api_azrael_transcript
 23310  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23285  GET              /api/azrael/voices                               api_azrael_voices
 23449  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11302  GET              /api/backoff-watch                               api_backoff_watch
 14743  POST             /api/backup/run                                  api_backup_run
 14709  GET              /api/backup/status                               api_backup_status
 14698  POST             /api/backup/system                               api_backup_system
 15451  GET              /api/bandwidth/live                              api_bandwidth_live
 15364  GET              /api/bookmarks                                   api_bookmarks_list
 11565  GET              /api/brain                                       api_brain
 11502  GET              /api/brain/alarms                                api_brain_alarms
 11487  GET              /api/brain/creator                               api_brain_creator
 11464  GET              /api/brain/graph                                 api_brain_graph
 11525  GET              /api/brain/growth                                api_brain_growth
 10293  GET              /api/brain/health                                api_brain_health
 23930  GET              /api/channel/categories                          api_channel_categories
 23936  POST             /api/channel/set                                 api_channel_set
 23746  GET              /api/channels/status                             api_channels_status
 22575  POST             /api/chat/send                                   api_chat_send
 14397  GET              /api/chat/send_status                            api_chat_send_status
 10828  GET              /api/checks                                      api_checks
 23251  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23234  GET              /api/clips                                       api_clips
 23267  POST/DELETE      /api/clips/clear                                 api_clips_clear
 22853  GET              /api/cohost                                      api_cohost
 22865  POST             /api/cohost/config                               api_cohost_config
 16050  GET              /api/community/stats                             api_community_stats
 24801  GET              /api/data/export                                 api_data_export
 22779  GET              /api/debug/threads                               api_debug_threads
 25651  GET              /api/defense/attacks                             api_defense_attacks
 25618  GET              /api/defense/crowdsec                            api_defense_crowdsec
 25636  GET              /api/defense/fail2ban                            api_defense_fail2ban
 25342  GET              /api/defense/overview                            api_defense_overview
 14805  POST             /api/discord/announce                            api_discord_announce
 14533  GET              /api/discord/clips_week                          api_discord_clips_week
 14749  GET              /api/discord/community                           api_discord_community
 14425  GET              /api/discord/invite                              api_discord_invite
 13999  GET              /api/discord/overview                            api_discord_overview
 14085  POST             /api/discord/webhook_test                        api_discord_webhook_test
 15433  GET              /api/events                                      api_events
 14580  GET              /api/events/stream                               api_events_stream
 16997  GET              /api/evolution/changelog                         api_evolution_changelog
 16982  GET              /api/evolution/history                           api_evolution_history
 16922  GET              /api/evolution/learned                           api_evolution_learned
 16944  GET              /api/evolution/proposals                         api_evolution_proposals
 16965  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 16912  POST             /api/evolution/run                               api_evolution_run
 17012  GET              /api/evolution/snapshots                         api_evolution_snapshots
 16877  GET              /api/evolution/status                            api_evolution_status
 15446  GET              /api/forecast/storage                            api_forecast_storage
 12516  GET              /api/freeai/status                               api_freeai_status
 13941  GET              /api/health                                      api_health
 15464  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15460  GET              /api/heatmap/recordings                          api_heatmap_recordings
 22902  GET              /api/highlights                                  api_highlights
 22914  POST             /api/highlights/config                           api_highlights_config
 23787  GET              /api/kick/channel                                api_kick_channel
 23808  POST             /api/kick/channel                                api_kick_channel_set
 13668  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13736  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13714  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13653  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13693  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23026  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23095  POST             /api/kickmod/config                              api_kickmod_config
 23140  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23154  GET              /api/kickmod/learned                             api_kickmod_learned
 23181  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23161  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 23492  POST             /api/kickmod/say                                 api_kickmod_say
 23468  POST             /api/kickmod/start                               api_kickmod_start
 23066  GET              /api/kickmod/status                              api_kickmod_status
 23479  POST             /api/kickmod/stop                                api_kickmod_stop
 10673  POST             /api/login                                       dashboard_login_submit
 16035  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12879  POST             /api/marketing/config                            api_marketing_config
 12904  GET              /api/marketing/preview                           api_marketing_preview
 12914  POST             /api/marketing/send-now                          api_marketing_send_now
 12853  GET              /api/marketing/status                            api_marketing_status
 12871  POST             /api/marketing/toggle                            api_marketing_toggle
 22929  GET              /api/moderation/feed                             api_moderation_feed
 13432  POST             /api/news/config                                 api_news_config
 13398  GET              /api/news/creators                               api_news_creators
 13409  POST             /api/news/creators/generate                      api_news_creators_generate
 13474  POST             /api/news/generate-now                           api_news_generate_now
 13469  GET              /api/news/items                                  api_news_items
 13460  GET              /api/news/preview                                api_news_preview
 13379  GET              /api/news/status                                 api_news_status
 13424  POST             /api/news/toggle                                 api_news_toggle
 16004  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14362  GET              /api/notify/status                               api_notify_status
 14373  POST             /api/notify/test                                 api_notify_test
 11060  GET              /api/outcomes                                    api_outcomes
 24407  POST             /api/overlay/config                              api_overlay_config
 24394  POST             /api/overlay/event                               api_overlay_event
 24299  GET              /api/overlay/state                               api_overlay_state
 11093  GET              /api/profile/<username>                          api_profile
 15644  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15472  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15598  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15575  GET              /api/proxy/trend                                 api_proxy_trend
 13353  GET              /api/public/stats                                api_public_stats
 10773  GET              /api/pulse                                       api_pulse
 14996  GET              /api/recording-attempts                          api_recording_attempts
 22510  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 22488  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 22529  POST             /api/restream/<int:rid>/start                    api_restream_start
 22800  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24261  GET              /api/restream/chatfeed                           api_restream_chatfeed
 22464  POST             /api/restream/create                             api_restream_create
 13744  GET              /api/restream/deck                               api_restream_deck
 12452  GET              /api/restream/health                             api_restream_health
 24283  POST             /api/restream/layout                             api_restream_layout
 22437  GET              /api/restream/list                               api_restream_list
 12421  POST             /api/restream/report                             api_restream_report
 22813  POST             /api/restream/start_all                          api_restream_start_all
 22839  POST             /api/restream/stop_all                           api_restream_stop_all
 12627  GET              /api/restream/testpush                           api_testpush_status
 12652  POST             /api/restream/testpush                           api_testpush_run
 16135  GET              /api/restream/verify                             api_restream_verify
 14511  GET              /api/retention/preview                           api_retention_preview
 14520  POST             /api/retention/run                               api_retention_run
 15349  GET              /api/search                                      api_search
 25389  GET              /api/selftest                                    api_selftest
 22546  GET              /api/shield/stats                                api_shield_stats
 10792  GET              /api/stats                                       api_stats
 15613  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15540  GET              /api/stats/tiktok-status                         api_tiktok_status
 24839  GET              /api/stats/timeline                              api_stats_timeline
 10869  GET              /api/storage                                     api_storage
 10876  POST             /api/storage/cleanup                             api_storage_cleanup
 15526  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12391  GET              /api/stream/timeline                             api_stream_timeline
 14073  GET              /api/stream/transcript                           api_stream_transcript
 24549  GET              /api/streamer/compare                            api_streamer_compare
 24748  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14472  GET              /api/streamer/detail                             api_streamer_detail
 24773  GET              /api/streamer/digest/<username>                  api_streamer_digest
 24653  GET              /api/streamer/dormant                            api_streamer_dormant
 24729  GET              /api/streamer/exists/<username>                  api_streamer_exists
 24608  GET              /api/streamer/journal/<username>                 api_streamer_journal
 24573  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 24633  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13908  GET              /api/streamers/wall                              api_streamers_wall
 10900  GET              /api/summary/preview                             api_summary_preview
 15061  GET              /api/system                                      api_system
 16083  GET              /api/system/check_timing                         api_check_timing
 16406  GET              /api/system/config_drift                         api_config_drift
 14109  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14220  GET              /api/system/preflight                            api_system_preflight
 14346  GET              /api/system/preflight_history                    api_system_preflight_history
 14645  GET              /api/system/resilience                           api_system_resilience
 15384  GET              /api/tags                                        api_tags_list
 10842  GET              /api/top                                         api_top
 12342  GET              /api/trackings                                   api_trackings
 15893  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 15926  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15420  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15633  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 15955  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15406  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 14835  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 14882  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 14911  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 14893  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10986  POST             /api/trackings/bulk                              api_trackings_bulk
 14850  GET              /api/trackings/export                            api_trackings_export
 10955  GET              /api/trackings/groups                            api_trackings_groups
 15388  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15682  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11357  GET              /api/trend-7d                                    api_trend_7d
 23299  GET              /api/tts/<fn>                                    api_tts_file
 16378  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16330  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 16354  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16308  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 24435  GET              /api/upload_window                               api_upload_window
 11074  GET              /api/userstats                                   api_userstats
 13485  GET              /api/version                                     api_version
 16229  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16250  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16262  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 16187  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 16211  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16165  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 29071  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15034  GET              /archive/<int:eid>/download                      archive_download
 15091  GET              /download/<int:recording_id>                     download
 14957  GET              /health                                          health
 22748  GET              /healthz                                         healthz
 10664  GET              /login                                           dashboard_login_page
 10694  GET              /logout                                          dashboard_logout
 10701  GET              /manifest.webmanifest                            pwa_manifest
 14137  GET              /metrics                                         api_prometheus_metrics
 24244  GET              /overlay                                         overlay_page
 10725  GET              /pwa-icon-<variant>.png                          pwa_icon
 10711  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (129)

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
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
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
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 26094  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 26553  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 26185  /assign_role            Rolle/Gruppe einem Mitglied geben
 26231  /ban                    Mitglied bannen
 26885  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 26809  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 26849  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 26834  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 26676  /clips                  Letzte Highlight-Clips eines Users
 26146  /create_category        Kategorie anlegen
 26115  /create_channel         Text-Channel anlegen (optional in Kategorie)
 26174  /create_group           Nutzergruppe (= Rolle) anlegen
 26157  /create_role            Rolle / Nutzergruppe anlegen
 26131  /create_voice           Voice-Channel anlegen
 26467  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 26583  /event                  Community-Event ankündigen (Admin) — mit Countdown
 26626  /events                 Kommende Community-Events anzeigen
 26722  /follow                 Bei Live-Gang eines Streamers gepingt werden
 26706  /help                   Alle Bot-Befehle anzeigen
 26220  /kick                   Mitglied kicken
 26449  /leaderboard            Top-10 der Community nach XP
 26662  /livenow                Welche getrackten User sind gerade live
 26692  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 26523  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 26255  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 26435  /rank                   Dein Level und Rang anzeigen
 26649  /recstatus              Aktuell laufende Aufnahmen
 26196  /remove_role            Rolle/Gruppe entfernen
 26108  /restream_status        Restream-Status
 26207  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 26400  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 26418  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 26748  /stats                  Statistik zu einem getrackten Streamer
 26020  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 27044  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 26941  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 26917  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 26242  /timeout                Mitglied stummschalten (Minuten)
 26820  /topstreamers           Rangliste der Streamer nach Aufnahmen
 26050  /track                  TikTok-User tracken
 26034  /tracklist              Getrackte TikTok-User dieses Servers
 26737  /unfollow               Live-Pings für einen Streamer abbestellen
 26083  /untrack                TikTok-User nicht mehr tracken
 26770  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 26794  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 27528  on_member_join
 27490  on_message
 27131  on_raw_reaction_add
 27563  on_ready
```

## Top-Level-Symbole in bot.py (560 Funktionen, 2 Klassen)

```
  2470-2471   _abo_key
  2491-2509   _abo_probe_dump
 24931-24941  _active_recorder_sync
 19734-19741  _ad_allowlist
 20856-20862  _agent_for
 24943-24961  _ai_calls_total_sync
 20865-20881  _ai_telemetry
 21363-21381  _alert
 27676-27726  _alert_monitor_loop
 28102-28164  _announce_loop
  3412-3415   _anthropic_key
  3422-3424   _anthropic_model
 10421-10424  _arg_int
  2462-2467   _as_dict
 17594-17599  _audio_cfg
 21517-21539  _audio_tap_cmd
 10585-10596  _auth_cookie
 10552-10581  _auth_guard
  1618-1623   _auto_on
 22413-22431  _auto_restream_loop
 29232-29247  _azrael_broadcast_reply
 29132-29154  _azrael_chat_reply
 29115-29129  _azrael_chat_should_reply
 13079-13097  _azrael_creator_take
 29160-29162  _azrael_gate_cfg
 20886-20900  _azrael_live_state
 24147-24161  _azrael_overlay_state
 21246-21300  _azrael_proactive_loop
 20705-20761  _azrael_reaction_to_chats
 29165-29172  _azrael_reply_all_chats
 29102-29112  _azrael_self_names
 29200-29229  _azrael_send_to
 20903-20924  _azrael_system
 27842-27845  _backup_active
 27923-27936  _backup_loop
 19622-19623  _badwords_path
 27641-27650  _brain_growth_loop
 11433-11460  _brain_growth_snapshot
  2398-2418   _brain_hint_delay
 11425-11427  _brain_history_for
  6827-6855   _brain_notify
 11402-11423  _brain_record
 11429-11431  _brain_stream_recent
 14559-14576  _browser_push
  6871-6958   _build_daily_summary
  2901-3081   _build_native_cmd
 17942-18129  _build_restream_cmd
  3125-3158   _build_ytdlp_cmd
 24883-24890  _cached_probe
  5649-5676   _can_stop_tracking
  1798-1820   _capture_set_cookies
 15730-15733  _cfg_get
 15736-15738  _cfg_set
 23891-23926  _channel_set_all
 17192-17195  _chat_connected
 17198-17214  _chat_disconnected
  8901-8912   _chat_is_forum
 17234-17236  _chat_sanitize
 17238-17247  _chat_src_ok
 17177-17189  _chat_stat
 17217-17220  _chat_stats_snapshot
  3687-3698   _check_ai_alive_sync
  3701-3713   _check_ai_models_sync
 24892-24905  _check_redis_alive_sync
 24907-24927  _check_redis_version_sync
 14437-14450  _ci_key
 12032-12075  _classify_pool_anonymity
 12078-12095  _classify_pool_anonymity_bg
   778-782    _claude_chat_sync_metered
 10446-10453  _client_ip
 28196-28223  _clip_prune
 28226-28236  _clip_recfile_for
 28752-28758  _clip_should_velocity
 28277-28359  _clip_to_discord
  3585-3594   _close_ai_session
 29276-29291  _cohost_broadcast
 29258-29262  _cohost_cfg
 29317-29329  _cohost_fire_highlight
 29265-29273  _cohost_gate
 29294-29314  _cohost_highlight
 28408-28442  _community_events_loop
 11256-11258  _conv_messages
  7251-7291   _cookie_alarm_loop
  1870-1874   _cookie_autorefresh_info
  1775-1779   _cookie_header
 14609-14641  _cpu_load_snapshot
  3895-3907   _create_index_safe
 13047-13062  _creator_activity
 13103-13126  _creator_dossier_generate
 13065-13076  _creator_facts_line
 25144-25250  _crowdsec_status
 25110-25141  _crowdsec_via_lapi
 24975-24993  _cscli_bin
 24999-25012  _cscli_path
  7144-7169   _daily_summary_loop
 25030-25047  _darf_journal_lesen
 10923-10951  _dashboard_track_group
 27653-27673  _db_maintenance_loop
  7116-7141   _db_vacuum_loop
 19757-19781  _detect_foreign_ad
  1356-1367   _diag_path_owner
 21152-21196  _director_finalize
 21963-21970  _director_for
 21101-21149  _director_mark
 28646-28681  _disc_automod_check
 28619-28625  _disc_state_get
 28628-28635  _disc_state_set
 25693-25706  _discord_guild_filesize_bytes
 25892-25901  _discord_invite
 28580-28616  _discord_live_thread
 21303-21315  _discord_notify
 25793-25818  _discord_ops_alert
 28478-28576  _discord_post_user
 25957-27638  _discord_run_once
 25831-25889  _discord_start
 28167-28173  _discord_stop
 25714-25716  _discord_upload_limit_label
 25709-25711  _discord_upload_limit_mb
  7172-7246   _disk_alarm_loop
 30658-30707  _disk_autoclean
 30710-30723  _disk_guard_loop
 30650-30655  _disk_pct
 17551-17553  _drawtext_chain
 15188-15190  _dump_all_threads
 11957-12021  _enrich_proxies_with_geo
  2015-2059   _ensure_cookie_file_netscape
 25904-25954  _ensure_discord_invite
 28373-28405  _ensure_error_channel
  8960-8963   _ensure_notify_topic
 12200-12237  _ensure_proxy_ready
  8914-8941   _ensure_topic
   641-643    _env_int
   646-648    _env_int_range
 28445-28475  _error_channel_loop
 21347-21360  _event_webhook
 16485-16491  _evo_build_dir
 16494-16501  _evo_version
 16777-16858  _evolution_cycle
 16510-16530  _evolution_llm_note
 16861-16871  _evolution_loop
 16533-16774  _evolution_write_build
  6269-6303   _extract_file_payload
  2147-2149   _extract_urls_from_streamurl_node
 25015-25022  _f2b_sudo_hint
 21383-21385  _faster_whisper_available
 19646-19658  _fetch_ldnoobw_de
 11846-11864  _fetch_proxy_list
 21797-21825  _fetch_tiktok_room_id
   712-715    _ff_cmd
 17714-17719  _find_chromium
  3118-3122   _find_external_recorder
  2152-2154   _find_stream_urls
 15781-15806  _fire_webhooks
  8027-8036   _fork_safe
   793-802    _freeai_chat_sync_metered
 25065-25107  _geo_lookup_ips
  3574-3583   _get_ai_session
  7861-7901   _get_live_info
  2688-2695   _get_resolve_semaphore
  8262-8628   _handle_single_tracking
 30502-30504  _hb
 30507-30524  _hb_while
 17252-17254  _highlight_cfg
 17257-17286  _highlight_observe
 17722-17727  _htmlov_screenshot_cmd
 21541-21551  _httpx_proxy
 15814-15826  _in_quiet_hours
 31537-31568  _install_fast_eventloop
 10316-10370  _install_fast_json
 15193-15209  _install_faulthandler
 22656-22665  _intel_ensure_schema
 22703-22738  _intel_index_loop
 22677-22687  _intel_index_one
 22668-22674  _intel_semantic
  5638-5647   _is_authorized
  8192-8198   _is_dead
  2137-2139   _is_hevc
 25050-25056  _is_private_ip
  1520-1527   _is_process_running
  6857-6868   _is_quiet_hours
  1160-1169   _is_upload_window
 10405-10418  _json_error_handler
  7074-7104   _kick_broadcaster_id
 12553-12572  _kick_channel_live
  6991-7033   _kick_follower_count
 13631-13644  _kick_oauth_exchange
 13647-13649  _kick_oauth_page
 13590-13594  _kick_redirect_public
 13585-13587  _kick_redirect_source
 13577-13582  _kick_redirect_uri
  6976-6978   _kick_slug
 13597-13628  _kick_user_token
  3944-3947   _kind_from_filename
 15843-15848  _latest_popularity
 19668-19674  _learned_load
 19665-19666  _learned_path
 19676-19684  _learned_save
 22178-22208  _live_react_loop
 21974-22167  _live_react_worker
 20764-20775  _live_transcript_push
 22169-22176  _live_users
 21199-21243  _living_title_loop
 19625-19633  _load_banned_words_file
  1696-1769   _load_cookies_dict
 27848-27920  _local_backup_scan
 10387-10401  _log_5xx
 18137-18149  _looks_like_codec_err
 18132-18134  _looks_like_source_expired
  8108-8138   _loop_fehler
 15213-15222  _loop_heartbeat
 30472-30499  _loop_lag_monitor
 15332-15335  _loop_not_ready
 15225-15293  _loop_watchdog_thread
 20644-20658  _loyalty_add
 20635-20641  _loyalty_get
 20661-20669  _loyalty_top
 16069-16071  _manual_donations_total
  8200-8201   _mark_dead
 12720-12749  _marketing_cfg
 12711-12717  _marketing_default_targets
 12706-12708  _marketing_enabled
 12763-12778  _marketing_flavor
 12833-12849  _marketing_loop
 12781-12791  _marketing_post_discord
 12794-12806  _marketing_post_telegram
 12809-12830  _marketing_publish
 12752-12756  _marketing_state_obj
 12759-12760  _marketing_state_save
 29179-29197  _maybe_handle_command
 30809-30833  _maybe_hype_clip
  3862-3885   _migrate_columns
 29456-29467  _mod_is_exempt
 29470-29475  _mod_warn_first
 29478-29481  _mod_warn_text
 17040-17048  _modlog
   913-915    _multistream_targets
  8039-8040   _nc_create_subprocess_exec
  8043-8044   _nc_create_subprocess_shell
 12944-12960  _news_cfg
 12931-12933  _news_enabled
 12998-13039  _news_facts
 13153-13175  _news_generate
 13358-13375  _news_loop
 12936-12941  _news_output_path
 13042-13044  _news_phrase
 13129-13150  _news_phrase_impl
 12973-12980  _news_read
 12963-12966  _news_state_obj
 12969-12970  _news_state_save
 12983-12995  _news_write
 17078-17080  _normalize_ingest
  2329-2346   _note_check_duration
  8954-8957   _notify_topic_name
 13541-13552  _oauth_redirect_env
 13568-13574  _oauth_redirect_source
 13555-13565  _oauth_redirect_uri
 20790-20798  _oracle_memories
 21056-21090  _oracle_memorize
 20801-20814  _oracle_persona
 20783-20787  _oracle_recent_text
 17377-17385  _ov_atomic_write
 17365-17371  _ov_bar
 19581-19593  _ov_clip_text
 17374-17375  _ov_oneline
 24211-24240  _overlay_push
 17668-17711  _overlay_render_size
 17139-17143  _overlay_session_reset
 24163-24166  _overlay_src_ok
 19744-19754  _own_invites
 17663-17665  _parse_size
 25258-25338  _parse_ssh_attacks
  7463-7496   _pause_resume_cmd
  1824-1868   _persist_refreshed_cookies
  1662-1694   _pick_checked_pull_proxy
 10482-10495  _pin_auth_value
 10541-10542  _pin_clear_fail
 10521-10524  _pin_locked
 10527-10538  _pin_note_fail
 10498-10518  _pin_ok
 24053-24055  _piper_available
 24018-24040  _piper_list_voices
 24060-24085  _piper_pick_model
 24097-24144  _piper_say
 24011-24015  _piper_voice_roots
 15743-15778  _post_json_threaded
 17642-17660  _probe_video_size
  1548-1565   _proc_is_recorder
 11944-11955  _proxy_geo_cache_put
 12171-12197  _proxy_pool_refresh_loop
  1628-1659   _proxy_report_recording
 15178-15180  _prune_stall_dumps
 13500-13538  _public_base_url
 13178-13299  _public_stats
 21318-21344  _push_notify
 10643-10645  _pwa_dir
 11915-11930  _quick_validate_proxy
 15809-15811  _quiet_hours_config
 10608-10641  _rate_guard
 20609-20615  _react_warn
  7947-7986   _reap_proc
  2369-2391   _record_check_outcome
   707-709    _redact_stream_urls
 12098-12168  _refresh_proxy_pool
 24043-24049  _resolve_piper_model
 14453-14468  _resolve_tracked_user
  2163-2253   _resolve_via_html
  2511-2665   _resolve_via_webcast_api_v2
  2728-2790   _resolve_via_ytdlp
 28798-28927  _resolve_youtube_ingest
 22247-22254  _restream_active_platforms
 17124-17135  _restream_active_sources
 21828-21927  _restream_chat_guardian
 17289-17361  _restream_chat_push
 17051-17063  _restream_enabled
 17730-17817  _restream_html_overlay_start
 17820-17833  _restream_html_overlay_stop
  1108-1110   _restream_layout_mode
 17089-17112  _restream_overlay_files
 22212-22244  _restream_platform_state
 22375-22410  _restream_resume_after_restart
 17881-17939  _restream_tts_enqueue_wav
 17604-17636  _restream_tts_feeder
 17601-17602  _restream_tts_fifo_path
 17836-17863  _restream_tts_start
 17865-17879  _restream_tts_stop
 22257-22372  _restream_verify_loop
 27813-27825  _retention_loop
 27772-27810  _retention_scan
  2473-2475   _room_is_abo
  6307-6424   _run_ai_call
 15316-15329  _run_async_from_flask
 25059-25062  _run_priv
 31525-31533  _run_selfcheck_and_exit
 27828-27839  _s3_client
  8203-8249   _safe_send
  4797-4813   _sample_net_throughput
 19635-19643  _save_banned_words_file
  2421-2448   _schedule_next_check
 27729-27769  _scheduler_loop
  3888-3892   _schema_pk
 15337-15342  _scraper_session
 29484-29523  _screen_full
 13957-13994  _sec_headers
  2142-2144   _select_stream_from_data_section
 31338-31522  _selfcheck
  8966-9000   _send_live_notice
  1183-1187   _should_defer_upload
 28239-28274  _shrink_for_discord
 10648-10660  _sicheres_ziel
 30730-30747  _sign_health_check
 30750-30769  _sign_health_loop
  8056-8067   _spawn
  8070-8100   _spawn_from_flask
 25382-25385  _st_befund
 21553-21794  _start_chat_listener
 15296-15313  _start_loop_watchdog
 13323-13349  _stats_loop
 13302-13305  _stats_output_path
 13308-13320  _stats_write
  8696-8710   _storage_cleanup_loop
 30789-30796  _story_for
  3180-3186   _stream_url_expiry
  3195-3201   _stream_url_is_fresh
  3188-3193   _stream_url_ttl
 19708-19715  _streamer_persona_get
 19690-19696  _streamer_personas_load
 19687-19688  _streamer_personas_path
 19698-19706  _streamer_personas_save
 17556-17560  _studio_chain
 27945-28067  _system_backup
 28070-28098  _system_backup_loop
 11867-11906  _test_proxy
 12594-12603  _testpush_cfg
 12606-12623  _testpush_exec
 12575-12591  _testpush_resolve_live
  8873-8883   _tg_topics_load_into_mem
  8870-8871   _tg_topics_path
  8885-8892   _tg_topics_save
 24677-24725  _tiktok_account_exists
 10456-10464  _token_ok
  8895-8899   _topic_forget
 15829-15840  _tracking_max_duration
  1414-1437   _try_attach_file_handler
 24087-24095  _tts_cleanup
 12531-12535  _tunnel_effective
 23513-23566  _twitch_channel_status
 29526-29669  _twitch_chat_loop
 29340-29443  _twitch_eventsub_loop
 16399-16402  _twitch_oauth_page
  1206-1219   _upload_queue_add
  1230-1232   _upload_queue_count
  1189-1198   _upload_queue_load
  1179-1181   _upload_queue_path
  1221-1228   _upload_queue_remove
  1200-1204   _upload_queue_save
  1234-1272   _upload_window_loop
  7920-7927   _uptime_s
 17066-17075  _url_host
   687-704    _url_ohne_zugang
   771-775    _usage_record_claude
  8141-8185   _verbindung_verloren
  7036-7064   _viewer_sample_loop
  7106-7113   _viewer_stats
 10545-10548  _wants_html
  7930-7944   _warn_empty_env
 30545-30640  _watchdog_loop
 29081-29089  _wchat_thank_ok
 21387-21417  _whisper_get_model
  8017-8024   _whisper_native_section
 20596-20602  _whisper_pool
 21486-21515  _whisper_segments
 21419-21483  _whisper_transcribe
 17387-17549  _write_restream_overlay
 29697-29770  _youtube_api_chat_loop
 23569-23672  _youtube_api_status
 23675-23742  _youtube_channel_status
 29773-29930  _youtube_chat_loop
 28933-28946  _youtube_restream_autoconfig
 28949-28973  _youtube_restream_autoconfig_inner
 29039-29067  _youtube_send
 23847-23888  _youtube_set_channel
 28976-29010  _yt_access_token
 29013-29028  _yt_live_chat_id
 29690-29694  _yt_oauth_configured
 29034-29036  _yt_sendrate_cfg
 29672-29687  _yt_timeout
  2712-2713   _ytdlp_detect_available
  2715-2726   _ytdlp_note_result
 15183-15185  _zombie_child_count
  7797-7821   about
  4063-4067   add_ai_log_entry
  3980-3983   add_archive_entry
  4910-4925   add_archive_rule
  4492-4526   add_recording
  4153-4170   add_tracking
  4587-4604   add_tracking_tag
  6427-6460   ai
  3727-3766   ai_chat
  3800-3810   ai_history_append
  3812-3817   ai_history_clear
  3789-3798   ai_history_load
  3774-3787   ai_rate_limit_check
  6489-6497   aireset
 20927-20946  azrael_chat
 29935-30057  brain_cmd
  3204-3388   build_recording_cmd
  4173-4250   bulk_add_trackings
  7294-7353   bulkadd
  8713-8853   check_all_trackings
  4337-4349   claim_live_transition
 19784-20539  class KickModerator
 18152-19468  class RestreamManager
 12282-12324  classify_proxy_anonymity
  6535-6733   cleanup
  5498-5539   cleanup_old_recordings
  4483-4490   clear_recording
 28684-28749  clip_moment
  5058-5101   cluster_failures
  4741-4790   compute_storage_forecast
  7416-7460   cookies_cmd
  4144-4150   count_trackings_for_chat
  4050-4061   decide_preferred_recorder
  3990-3993   delete_archive_entry
  4927-4935   delete_archive_rule
  5964-6111   diag
 30169-30230  einnahmen_cmd
  4735-4738   find_recordings_by_fingerprint
  4011-4027   finish_recording_attempt
  4282-4292   get_all_active_trackings
  4089-4092   get_all_checks
  4528-4531   get_all_recordings
  4629-4639   get_all_tags_with_counts
  4712-4715   get_annotations_for_recording
  3985-3988   get_archive_entry
  4705-4708   get_bookmarked_recordings
  1891-2008   get_cookie_health
  4578-4584   get_event_log
  4034-4048   get_last_recording_attempt
  2793-2898   get_live_status
  5261-5264   get_manual_recordings
  4720-4723   get_or_compute_inspect_sync
  5574-5618   get_outcome_breakdown
  4686-4694   get_priority_poll_interval
  4888-4897   get_profile_snapshots
  4069-4079   get_recent_ai_log
  4029-4032   get_recent_recording_attempts
  4533-4536   get_recording_by_id
  4698-4701   get_recording_note
  3522-3545   get_redis
  4120-4136   get_stats
  5465-5496   get_storage_stats
  4619-4627   get_tags_for_tracking
  5028-5042   get_tiktok_status_distribution
  4673-4684   get_tracking_priority
  4351-4360   get_tracking_state
  4278-4280   get_trackings_for_group
  5277-5280   get_trash_recordings
  9621-10284  handle_recording_finished
  3910-3935   init_db
  5388-5442   inspect_stream_url
 24206-24208  is_revenue_platform
  4900-4908   list_archive_rules
  5768-5806   live
  8252-8260   live_check_worker
  3597-3631   llm_chat
  3654-3682   llm_chat_sync
  3639-3651   llm_list_models
  4544-4570   log_event
  1482-1515   log_recording_failure
  7610-7659   logs_cmd
 30837-31328  main
  6463-6486   on_ai_media
  7736-7762   on_ai_reply
  7765-7794   on_azrael_mention
  7826-7856   on_callback
 20949-21053  oracle_handle
  7499-7502   pause_tracking
  5628-5633   profile_keyboard
  5349-5385   quick_restart_tracking
  7561-7607   quota
  8630-8693   reaper_loop
  5024-5026   record_tiktok_status
  6502-6532   recstatus
  3547-3555   redis_get_json
  3557-3563   redis_set_json
  4252-4276   remove_tracking
  4606-4617   remove_tracking_tag
 30233-30243  report_cmd
 12327-12329  report_proxy_result
  2256-2283   resolve_tiktok_live_stream
  5272-5275   restore_recording
  7505-7508   resume_tracking
  4938-5018   run_archive_rules
 30246-30452  run_bot
 15105-15152  run_flask
  4816-4861   sample_bandwidth_for_active
  4867-4886   save_profile_snapshot
  4081-4087   save_tiktok_check
  4475-4481   set_recording_file
  4295-4333   set_tracking_paused
  4642-4671   set_tracking_priority
  5267-5270   soft_delete_recording
  9006-9619   split_and_send_video
  5681-5723   start
  3995-4009   start_recording_attempt
  6736-6774   stats
  5242-5259   stop_manual_recording
  7511-7558   stoprec
  6961-6969   summary_cmd
  7662-7733   sysres
  6113-6257   teststream
  5725-5766   tiktok
  7356-7413   topusers
  5843-5900   track
  5808-5840   track_exact
  5914-5962   tracklist
  5108-5240   trigger_manual_recording
  4436-4473   try_acquire_recording_lock
  5283-5342   universal_search
  5902-5912   untrack
 30060-30166  update_cmd
  4730-4733   update_recording_fingerprint
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
donationsdb.py         manual_rows, manual_total, parse_eur
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
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
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
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
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
